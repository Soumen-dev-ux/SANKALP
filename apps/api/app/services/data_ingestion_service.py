from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.region import Region
from app.models.demographic import Demographic
from app.models.infrastructure import Infrastructure
from app.models.government_project import GovernmentProject


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_region(db: Session, region_id: int) -> None:
    region = db.query(Region).filter(Region.id == region_id).first()

    if not region:
        raise ValueError(
            f"Region with id {region_id} does not exist."
        )


def ingest_demographic(
    db: Session,
    data: dict[str, Any],
) -> str:
    region_id = data["region_id"]

    validate_region(db, region_id)

    existing = (
        db.query(Demographic)
        .filter(Demographic.region_id == region_id)
        .first()
    )

    if existing:
        return f"Skipped demographic for region {region_id}"

    record = Demographic(**data)

    db.add(record)
    return f"Inserted demographic for region {region_id}"


def ingest_infrastructure(
    db: Session,
    data: dict[str, Any],
) -> str:
    region_id = data["region_id"]

    validate_region(db, region_id)

    existing = (
        db.query(Infrastructure)
        .filter(
            Infrastructure.region_id == region_id,
            Infrastructure.category == data["category"],
            Infrastructure.infrastructure_type
            == data["infrastructure_type"],
            Infrastructure.name == data.get("name"),
        )
        .first()
    )

    if existing:
        return (
            f"Skipped infrastructure "
            f"'{data.get('name', data['infrastructure_type'])}'"
        )

    record = Infrastructure(**data)

    db.add(record)

    return (
        f"Inserted infrastructure "
        f"'{data.get('name', data['infrastructure_type'])}'"
    )


def ingest_project(
    db: Session,
    data: dict[str, Any],
) -> str:
    region_id = data["region_id"]

    validate_region(db, region_id)

    existing = (
        db.query(GovernmentProject)
        .filter(
            GovernmentProject.region_id == region_id,
            GovernmentProject.name == data["name"],
        )
        .first()
    )

    if existing:
        return f"Skipped project '{data['name']}'"

    normalized_data = data.copy()

    normalized_data["start_date"] = parse_datetime(
        normalized_data.get("start_date")
    )

    normalized_data["expected_completion_date"] = parse_datetime(
        normalized_data.get("expected_completion_date")
    )

    normalized_data["actual_completion_date"] = parse_datetime(
        normalized_data.get("actual_completion_date")
    )

    record = GovernmentProject(**normalized_data)

    db.add(record)

    return f"Inserted project '{data['name']}'"