from sqlalchemy import Column
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.region import Region


class CitizenRequest(Base):
    __tablename__ = "citizen_requests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    anonymous_reference: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    raw_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    language: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    intent: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    issue: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    region_id: Mapped[int | None] = mapped_column(
        ForeignKey("regions.id"),
        nullable=True,
        index=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="submitted",
        index=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="web",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    region: Mapped["Region | None"] = relationship(
        "Region",
        backref="citizen_requests",
    )

    review_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="not_required",
        index=True,
    )

    reviewer_note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    reviewed_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    reviewed_issue: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    reviewed_location: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    review_actions = relationship(
        "HumanReviewAction",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    @property
    def request_id(self) -> int:
        return self.id

    @property
    def location_text(self) -> str | None:
        return self.reviewed_location

    @property
    def confidence_review_required(self) -> bool:
        return self.review_status == "pending"