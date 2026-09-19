from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
)

from app.db.base import Base


class Demographic(Base):

    __tablename__ = "demographics"

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

    population = Column(
        Integer,
        nullable=False,
    )

    population_density = Column(
        Float,
        nullable=True,
    )

    income_index = Column(
        Float,
        nullable=True,
    )

    age_0_14_percent = Column(
        Float,
        nullable=True,
    )

    age_15_24_percent = Column(
        Float,
        nullable=True,
    )

    age_25_64_percent = Column(
        Float,
        nullable=True,
    )

    age_65_plus_percent = Column(
        Float,
        nullable=True,
    )

    growth_rate = Column(
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