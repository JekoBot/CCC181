"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "dev-only-change-me"

# The items students can claim, and the sizes they can pick.
# Replace both with the real ones from the sizing form.
SERVICES = [
    {"id": 1, "name": "PE shirt"},
    {"id": 2, "name": "PE pants"},
]
SIZES = ["XS", "S", "M", "L", "XL", "2XL"]

# Sample data for the demo. A real app would load this from a database later.
# Each ticket: number, name, section, items, status
# items is a list of {"service_id", "size"}, one or two entries
# status is one of: waiting, called, served, no-show
TICKETS = [
    {"number": 1, "name": "Ana", "section": "BSCS 1A",
     "items": [{"service_id": 1, "size": "M"}, {"service_id": 2, "size": "L"}],
     "status": "waiting"},
    {"number": 2, "name": "Ben", "section": "BSCS 1B",
     "items": [{"service_id": 1, "size": "L"}],
     "status": "waiting"},
]


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, sizes=SIZES, form={})


@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip()
    section = form.get("section", "").strip()
    item1 = form.get("item1", type=int)
    size1 = form.get("size1", "")
    item2 = form.get("item2", type=int)
    size2 = form.get("size2", "")
    valid_items = [s["id"] for s in SERVICES]

    errors = {}
    if not name:
        errors["name"] = "Enter your name."
    if not section:
        errors["section"] = "Enter your class section."
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
        return render_template("join.html", services=SERVICES, sizes=SIZES,
                               form=form, errors=errors), 400

    items = [{"service_id": item1, "size": size1}]
    if item2 is not None:
        items.append({"service_id": item2, "size": size2})

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1
    TICKETS.append({"number": number, "name": name, "section": section,
                    "items": items, "status": "waiting"})
    flash(f"You joined the queue. Your queue number is #{number}.", "success")
    return redirect(url_for("ticket", ticket_id=number))

STATUS_LABELS = {"waiting": "Waiting", "called": "Called", "served": "Served",
                 "no-show": "No-show", "left": "Left the queue"}
STATUS_BADGES = {"waiting": "text-bg-warning", "called": "text-bg-success",
                 "served": "text-bg-secondary", "no-show": "text-bg-danger",
                 "left": "text-bg-secondary"}


def find_ticket(ticket_id):
    return next((t for t in TICKETS if t["number"] == ticket_id), None)


def people_ahead(t):
    """Students still waiting with an earlier queue number. One queue for everyone."""
    return sum(1 for x in TICKETS
               if x["status"] == "waiting" and x["number"] < t["number"])


def position_text(t, ahead):
    if t["status"] == "waiting":
        if ahead == 0:
            return "You're next!"
        return "1 person ahead of you" if ahead == 1 else f"{ahead} people ahead of you"
    if t["status"] == "called":
        return "It's your turn. Please come to the counter now."
    if t["status"] == "served":
        return "You've been served. Thank you!"
    return "You are no longer in the queue."



@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    ahead = people_ahead(t)
    names = {s["id"]: s["name"] for s in SERVICES}
    items = [{"name": names[i["service_id"]], "size": i["size"]} for i in t["items"]]
    return render_template("ticket.html", ticket=t, items=items,
                           status_label=STATUS_LABELS[t["status"]],
                           badge_class=STATUS_BADGES[t["status"]],
                           position_text=position_text(t, ahead))


@app.post("/queue/<int:ticket_id>/leave")
def leave_queue(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    if t["status"] in ("waiting", "called"):
        t["status"] = "left"
        flash("You left the queue.", "info")
    else:
        flash("This queue number is no longer active.", "warning")
    return redirect(url_for("index"))


@app.get("/queue/<int:ticket_id>/status.json")
def ticket_status(ticket_id):
    t = find_ticket(ticket_id)
    if t is None:
        abort(404)
    ahead = people_ahead(t)
    return {
        "status": t["status"],
        "status_label": STATUS_LABELS[t["status"]],
        "badge_class": STATUS_BADGES[t["status"]],
        "position_text": position_text(t, ahead),
        "ahead": ahead,
        "active": t["status"] in ("waiting", "called"),
    }


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)
    names = {s["id"]: s["name"] for s in SERVICES}

    def wants(t):
        return service_id is None or any(i["service_id"] == service_id for i in t["items"])

    active = [t for t in TICKETS if t["status"] in ("waiting", "called") and wants(t)]
    active.sort(key=lambda t: t["number"])

    rows = []
    for t in active:
        first = t["items"][0]
        second = t["items"][1] if len(t["items"]) > 1 else None
        rows.append({
            "number": t["number"], "name": t["name"], "section": t["section"],
            "item1": names[first["service_id"]], "size1": first["size"],
            "item2": names[second["service_id"]] if second else "-",
            "size2": second["size"] if second else "-",
            "status": t["status"],
            "status_label": STATUS_LABELS[t["status"]],
            "badge_class": STATUS_BADGES[t["status"]],
        })

    waiting_count = sum(1 for r in rows if r["status"] == "waiting")
    now_serving = [r for r in rows if r["status"] == "called"]
    # ★ How many students are waiting for each item
    counts = {s["id"]: sum(1 for t in TICKETS
                           if t["status"] == "waiting"
                           and any(i["service_id"] == s["id"] for i in t["items"]))
              for s in SERVICES}
    return render_template("staff.html", rows=rows, services=SERVICES, selected=service_id,
                           waiting_count=waiting_count, now_serving=now_serving, counts=counts)


@app.post("/staff/call-next")
def call_next():
    service_id = request.form.get("service_id", type=int)
    waiting = [t for t in TICKETS
               if t["status"] == "waiting"
               and (service_id is None or any(i["service_id"] == service_id for i in t["items"]))]
    if not waiting:
        flash("No one is waiting.", "warning")
    else:
        nxt = min(waiting, key=lambda t: t["number"])
        nxt["status"] = "called"
        flash(f"Queue number #{nxt['number']} ({nxt['name']}) called.", "info")
    return redirect(url_for("staff_dashboard", service_id=service_id))


@app.post("/staff/tickets/<int:ticket_id>/<action>")
def staff_action(ticket_id, action):
    new_status = {"serve": "served", "no-show": "no-show"}.get(action)
    t = find_ticket(ticket_id)
    if t is None or new_status is None:
        abort(404)
    if t["status"] != "called":
        flash(f"Queue number #{ticket_id} must be called first.", "warning")
    else:
        t["status"] = new_status
        flash(f"Queue number #{ticket_id} marked {STATUS_LABELS[new_status].lower()}.", "info")
    return redirect(url_for("staff_dashboard",
                            service_id=request.form.get("service_id", type=int)))