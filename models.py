from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (CheckConstraint, DateTime, ForeignKey, Identity, Index,
                        SmallInteger, String, UniqueConstraint, func, text, true)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    active: Mapped[bool] = mapped_column(default=True, server_default=true())

    ticket_items: Mapped[list["TicketItem"]] = relationship(back_populates="item")


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)  # the queue number
    name: Mapped[str] = mapped_column(String(80))
    section: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    session_id: Mapped[str] = mapped_column(String(64))

    items: Mapped[list["TicketItem"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan",
        passive_deletes=True, order_by="TicketItem.position")

    __table_args__ = (
        CheckConstraint("status IN ('waiting', 'called', 'served', 'no-show', 'left')",
                        name="ck_tickets_status"),
        CheckConstraint("length(trim(name)) > 0", name="ck_tickets_name_not_blank"),
        CheckConstraint("length(trim(section)) > 0", name="ck_tickets_section_not_blank"),
        # One active ticket per browser session
        Index("one_active_ticket_per_session", "session_id", unique=True,
              postgresql_where=text("status IN ('waiting', 'called')")),
        # "Call next" and the waiting list read only waiting tickets, oldest first
        Index("ix_tickets_waiting", "joined_at",
              postgresql_where=text("status = 'waiting'")),
    )


class TicketItem(db.Model):
    __tablename__ = "ticket_items"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="RESTRICT"))
    size: Mapped[str] = mapped_column(String(3))
    position: Mapped[int] = mapped_column(SmallInteger)

    ticket: Mapped["Ticket"] = relationship(back_populates="items")
    item: Mapped["Item"] = relationship(back_populates="ticket_items")

    __table_args__ = (
        CheckConstraint("size IN ('XS', 'S', 'M', 'L', 'XL', '2XL')", name="ck_ticket_items_size"),
        CheckConstraint("position IN (1, 2)", name="ck_ticket_items_position"),
        UniqueConstraint("ticket_id", "position", name="uq_ticket_items_ticket_position"),
        UniqueConstraint("ticket_id", "item_id", name="uq_ticket_items_ticket_item"),
    )