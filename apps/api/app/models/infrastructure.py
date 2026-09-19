from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)

from app.db.base import Base


class Infrastructure(Base):

    __tablename__ = "infrastructure"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    region_id = Column(
        Integer,
        ForeignKey("regions.id"),
        nullable=False,
        index=True,
    )

    category = Column(
        String(100),
        nullable=False,
        index=True,
    )

    infrastructure_type = Column(
        String(100),
        nullable=False,
    )

    name = Column(
        String(255),
        nullable=True,
    )

    capacity = Column(
        Integer,
        nullable=True,
    )

    coverage_percent = Column(
        Float,
        nullable=True,
    )

    quality_score = Column(
        Float,
        nullable=True,
    )

    operational = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    latitude = Column(
        Float,
        nullable=True,
    )

    longitude = Column(
        Float,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )