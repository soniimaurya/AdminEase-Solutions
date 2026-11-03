from datetime import datetime, date, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    name: Mapped[str] = mapped_column(
        String(150), index=True
    )

    email: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )

    company: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )

    source: Mapped[str | None] = mapped_column(
        String(80), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30), default="New", index=True
    )

    notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now
    )

    follow_ups: Mapped[list["FollowUp"]] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan"
    )

    interactions: Mapped[list["Interaction"]] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan"
    )


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"), index=True
    )

    due_date: Mapped[date] = mapped_column(
        Date, index=True
    )

    description: Mapped[str] = mapped_column(
        String(500)
    )

    status: Mapped[str] = mapped_column(
        String(20), default="Pending", index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    lead: Mapped["Lead"] = relationship(
        back_populates="follow_ups"
    )


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id"), index=True
    )

    interaction_type: Mapped[str] = mapped_column(
        String(50)
    )

    details: Mapped[str] = mapped_column(
        Text
    )

    interacted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    lead: Mapped["Lead"] = relationship(
        back_populates="interactions"
    )