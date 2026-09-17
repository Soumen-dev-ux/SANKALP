from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    country_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        index=True,
    )

    parent_region_id: Mapped[int | None] = mapped_column(
        ForeignKey("regions.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    parent: Mapped["Region | None"] = relationship(
        "Region",
        remote_side=[id],
        back_populates="children",
    )

    children: Mapped[list["Region"]] = relationship(
        "Region",
        back_populates="parent",
    )