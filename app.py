"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
import os
import secrets

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, timezone
from sqlalchemy import func, update

from models import Item, Ticket, TicketItem, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8)) 


@app.template_filter("local")
def local_time(value):
    """Show a database time in Philippine time, e.g. Nov 10, 08:01 AM."""
    return value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p") if value else ""

@app.cli.command("seed")
def seed():
    """Add the starting items if they are not there yet."""
    for name in ["PE shirt", "PE pants"]:
        if db.session.scalar(db.select(Item).filter_by(name=name)) is None:
            db.session.add(Item(name=name))
    db.session.commit()
    print("Items are ready.")


SIZES = ["XS", "S", "M", "L", "XL", "2XL"]

STATUS_LABELS = {"waiting": "Waiting", "called": "Called", "served": "Served",
                 "no-show": "No-show", "left": "Left the queue"}
STATUS_BADGES = {"waiting": "text-bg-warning", "called": "text-bg-success",
                 "served": "text-bg-secondary", "no-show": "text-bg-danger",
                 "left": "text-bg-secondary"}


def active_items():
    stmt = db.select(Item).filter_by(active=True).order_by(Item.name)
    return db.session.scalars(stmt).all()

def all_items():
    return db.session.scalars(db.select(Item).order_by(Item.name)).all()


def change_status(ticket_id, expected, new_status):
    """Update a ticket only if it still has an expected status. True if it changed."""
    values = {"status": new_status}
    if new_status == "called":
        values["called_at"] = func.now()
    result = db.session.execute(
        update(Ticket).where(Ticket.id == ticket_id, Ticket.status.in_(expected)).values(**values))
    db.session.commit()
    return result.rowcount == 1


def active_ticket():
    """The ticket this browser joined with, if it is still waiting or called."""
    token = session.get("session_id")
    if not token:
        return None
    return db.session.scalar(
        db.select(Ticket).where(Ticket.session_id == token,
                                Ticket.status.in_(["waiting", "called"])))


def people_ahead(t):
    """Waiting tickets with a smaller id. The id is unique and always in join order."""
    stmt = (db.select(func.count()).select_from(Ticket)
            .where(Ticket.status == "waiting", Ticket.id < t.id))
    return db.session.scalar(stmt)



GO_TO_VENUE_AHEAD = 5  # tell students to head to the venue when fewer than this many are ahead


def should_go_to_venue(t, ahead):
    return t.status in ("waiting", "called") and ahead < GO_TO_VENUE_AHEAD


def position_text(t, ahead):
    if t.status == "waiting":
        if ahead == 0:
            return "You're next!"
        return "1 person ahead of you" if ahead == 1 else f"{ahead} people ahead of you"
    if t.status == "called":
        return "It's your turn. Please come to the counter now."
    if t.status == "served":
        return "You've been served. Thank you!"
    return "You are no longer in the queue."


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    t = active_ticket()
    if t:
        flash("You are already in the queue. To get a new queue number, please leave the queue first.", "info")
        return redirect(url_for("ticket", ticket_id=t.id))
    return render_template("join.html", services=active_items(), sizes=SIZES, form={})


@app.post("/join")
def join():
    t = active_ticket()
    if t:
        flash("You are already in the queue. To get a new queue number, please leave the queue first.", "info")
        return redirect(url_for("ticket", ticket_id=t.id))

    form = request.form
    name = form.get("name", "").strip()
    section = form.get("section", "").strip()
    item1 = form.get("item1", type=int)
    size1 = form.get("size1", "")
    item2 = form.get("item2", type=int)
    size2 = form.get("size2", "")
    valid_items = {i.id for i in active_items()}

    errors = {}
    if not name or len(name) > 80:
        errors["name"] = "Enter your name (up to 80 characters)."
    if not section or len(section) > 30:
        errors["section"] = "Enter your class section (up to 30 characters)."
    if item1 not in valid_items:
        errors["item1"] = "Choose an item."
    if size1 not in SIZES:
        errors["size1"] = "Choose a size."

    # Item 2 is optional, but if either field is filled in, both must be valid.
    if item2 is not None or size2:
        if item2 not in valid_items:
            errors["item2"] = "Choose an item, or clear the size."
        elif item2 == item1:
            errors["item2"] = "Choose a different item from Item 1."
        if size2 not in SIZES:
            errors["size2"] = "Choose a size."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template("join.html", services=active_items(), sizes=SIZES,
                               form=form, errors=errors), 400

    token = session.get("session_id") or secrets.token_urlsafe(16)
    session["session_id"] = token
    session.permanent = True  # keeps the cookie after the browser closes

    ticket = Ticket(name=name, section=section, session_id=token)
    ticket.items.append(TicketItem(item_id=item1, size=size1, position=1))
    if item2 is not None:
        ticket.items.append(TicketItem(item_id=item2, size=size2, position=2))
    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # the session must be rolled back before it can be used again
        t = active_ticket()
        if t:  # two quick submits from the same browser: the unique index refused the second
            return redirect(url_for("ticket", ticket_id=t.id))
        flash("Something went wrong saving your ticket. Please try again.", "danger")
        return render_template("join.html", services=active_items(), sizes=SIZES,
                               form=form, errors={}), 409

    flash(f"You joined the queue. Your queue number is #{ticket.id}.", "success")
    return redirect(url_for("ticket", ticket_id=ticket.id))


@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    items = [{"name": ti.item.name, "size": ti.size} for ti in t.items]
    return render_template("ticket.html", ticket=t, items=items,
                           status_label=STATUS_LABELS[t.status],
                           badge_class=STATUS_BADGES[t.status],
                           position_text=position_text(t, ahead),
                           go_to_venue=should_go_to_venue(t, ahead))
                           


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    if t.session_id != session.get("session_id"):
        abort(403)  # only the browser that joined can leave
    if change_status(ticket_id, ("waiting", "called"), "left"):  # soft delete: the row stays
        flash("You left the queue.", "info")
    else:
        flash("This queue number is no longer active.", "warning")
    return redirect(url_for("index"))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    ahead = people_ahead(t)
    return {
        "status": t.status,
        "status_label": STATUS_LABELS[t.status],
        "badge_class": STATUS_BADGES[t.status],
        "position_text": position_text(t, ahead),
        "ahead": ahead,
        "go_to_venue": should_go_to_venue(t, ahead),
        "active": t.status in ("waiting", "called"),
    }


@app.get("/staff")
def staff_dashboard():
    item_id = request.args.get("service_id", type=int)
    stmt = (db.select(Ticket)
            .where(Ticket.status.in_(["waiting", "called"]))
            .order_by(Ticket.joined_at, Ticket.id))
    if item_id:
        stmt = stmt.where(Ticket.items.any(TicketItem.item_id == item_id))

    rows = []
    for t in db.session.scalars(stmt).all():
        first = t.items[0]
        second = t.items[1] if len(t.items) > 1 else None
        rows.append({
            "number": t.id, "name": t.name, "section": t.section,
            "item1": first.item.name, "size1": first.size,
            "item2": second.item.name if second else "-",
            "size2": second.size if second else "-",
            "joined_at": t.joined_at,
            "status": t.status,
            "status_label": STATUS_LABELS[t.status],
            "badge_class": STATUS_BADGES[t.status],
        })

    waiting_count = sum(1 for r in rows if r["status"] == "waiting")
    now_serving = [r for r in rows if r["status"] == "called"]
    items = all_items()
    # ★ How many students are waiting for each item
    counts = {i.id: db.session.scalar(
                  db.select(func.count(Ticket.id))
                  .where(Ticket.status == "waiting",
                         Ticket.items.any(TicketItem.item_id == i.id)))
              for i in items}
    return render_template("staff.html", rows=rows, services=items, selected=item_id,
                           waiting_count=waiting_count, now_serving=now_serving, counts=counts)


@app.post("/staff/call-next")
def call_next():
    item_id = request.form.get("service_id", type=int)
    stmt = (db.select(Ticket).where(Ticket.status == "waiting")
            .order_by(Ticket.joined_at, Ticket.id).limit(1))
    if item_id:
        stmt = stmt.where(Ticket.items.any(TicketItem.item_id == item_id))
    nxt = db.session.scalar(stmt)
    if nxt is None:
        flash("No one is waiting.", "warning")
    elif change_status(nxt.id, ("waiting",), "called"):
        flash(f"Queue number #{nxt.id} ({nxt.name}) called.", "info")
    else:
        flash("That ticket just changed. Please try again.", "warning")
    return redirect(url_for("staff_dashboard", service_id=item_id))


STAFF_ACTIONS = {"serve": "served", "no-show": "no-show"}


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = STAFF_ACTIONS.get(action)
    if new_status is None:
        abort(404)
    db.get_or_404(Ticket, ticket_id)
    if change_status(ticket_id, ("called",), new_status):
        flash(f"Queue number #{ticket_id} marked {STATUS_LABELS[new_status].lower()}.", "info")
    else:
        flash(f"Queue number #{ticket_id} must be called first.", "warning")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))


@app.post("/staff/delete/<int:ticket_id>")
def delete_ticket(ticket_id):
    t = db.get_or_404(Ticket, ticket_id)
    db.session.delete(t)  # hard delete: its item lines go too (ON DELETE CASCADE)
    db.session.commit()
    flash(f"Queue number #{ticket_id} was deleted.", "warning")
    return redirect(url_for("staff_dashboard"))

@app.get("/staff/items")
def items_list():
    items = all_items()
    counts = {i.id: db.session.scalar(
                  db.select(func.count(TicketItem.id)).where(TicketItem.item_id == i.id))
              for i in items}
    return render_template("items.html", items=items, counts=counts)


@app.post("/staff/items")
def item_create():
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter an item name (up to 60 characters).", "danger")
        return redirect(url_for("items_list"))
    db.session.add(Item(name=name))
    try:
        db.session.commit()
        flash(f"Item “{name}” added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"An item named “{name}” already exists.", "danger")
    return redirect(url_for("items_list"))


@app.post("/staff/items/<int:item_id>/edit")
def item_edit(item_id):
    item = db.get_or_404(Item, item_id)
    name = request.form.get("name", "").strip()
    if not name or len(name) > 60:
        flash("Enter an item name (up to 60 characters).", "danger")
        return redirect(url_for("items_list"))
    item.name = name
    item.active = request.form.get("active") == "on"  # an unticked box is not sent at all
    try:
        db.session.commit()
        flash(f"Item “{name}” saved.", "success")
    except IntegrityError:
        db.session.rollback()
        flash(f"An item named “{name}” already exists.", "danger")
    return redirect(url_for("items_list"))


@app.post("/staff/items/<int:item_id>/delete")
def item_delete(item_id):
    item = db.get_or_404(Item, item_id)
    name = item.name
    if item.ticket_items:
        flash(f"“{name}” has tickets, so it cannot be deleted. Switch it off instead.", "danger")
    else:
        db.session.delete(item)
        db.session.commit()
        flash(f"Item “{name}” deleted.", "warning")
    return redirect(url_for("items_list"))

if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
