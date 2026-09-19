from sqlalchemy.orm import Session

from app.models.region import Region
from app.models.demographic import Demographic
from app.models.infrastructure import Infrastructure
from app.models.government_project import GovernmentProject
from app.models.citizen_request import CitizenRequest


def get_regions(db: Session):
    return (
        db.query(Region)
        .order_by(Region.id)
        .all()
    )


def get_region(
    db: Session,
    region_id: int,
):
    return (
        db.query(Region)
        .filter(Region.id == region_id)
        .first()
    )


def get_region_demographics(
    db: Session,
    region_id: int,
):
    return (
        db.query(Demographic)
        .filter(Demographic.region_id == region_id)
        .all()
    )


def get_region_infrastructure(
    db: Session,
    region_id: int,
):
    return (
        db.query(Infrastructure)
        .filter(Infrastructure.region_id == region_id)
        .order_by(Infrastructure.category)
        .all()
    )


def get_region_projects(
    db: Session,
    region_id: int,
):
    return (
        db.query(GovernmentProject)
        .filter(GovernmentProject.region_id == region_id)
        .order_by(GovernmentProject.id)
        .all()
    )


def get_region_requests(
    db: Session,
    region_id: int,
):
    return (
        db.query(CitizenRequest)
        .filter(CitizenRequest.region_id == region_id)
        .order_by(CitizenRequest.created_at.desc())
        .all()
    )


def get_region_summary(
    db: Session,
    region_id: int,
):
    region = get_region(db, region_id)

    if not region:
        return None

    demographics_count = (
        db.query(Demographic)
        .filter(Demographic.region_id == region_id)
        .count()
    )

    infrastructure_count = (
        db.query(Infrastructure)
        .filter(Infrastructure.region_id == region_id)
        .count()
    )

    project_count = (
        db.query(GovernmentProject)
        .filter(GovernmentProject.region_id == region_id)
        .count()
    )

    request_count = (
        db.query(CitizenRequest)
        .filter(CitizenRequest.region_id == region_id)
        .count()
    )

    return {
        "id": region.id,
        "name": region.name,
        "demographics_count": demographics_count,
        "infrastructure_count": infrastructure_count,
        "project_count": project_count,
        "request_count": request_count,
    }