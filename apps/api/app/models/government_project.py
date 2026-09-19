from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from app.db.base import Base


class GovernmentProject(Base):

    __tablename__ = "government_projects"

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

    name = Column(
        String(255),
        nullable=False,
    )

    category = Column(
        String(100),
        nullable=False,
        index=True,
    )

    description = Column(
        Text,
        nullable=True,
    )

    status = Column(
        String(50),
        nullable=False,
        index=True,
    )

    budget = Column(
        Float,
        nullable=True,
    )

    implementing_agency = Column(
        String(255),
        nullable=True,
    )

    start_date = Column(
        DateTime,
        nullable=True,
    )

    expected_completion_date = Column(
        DateTime,
        nullable=True,
    )

    actual_completion_date = Column(
        DateTime,
        nullable=True,
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