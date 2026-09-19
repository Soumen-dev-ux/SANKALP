from sqlalchemy.orm import Session

from app.models.infrastructure import Infrastructure
from app.schemas.infrastructure import InfrastructureCreate


def create_infrastructure(
    db: Session,
    infrastructure_data: InfrastructureCreate,
) -> Infrastructure:

    infrastructure = Infrastructure(
        region_id=infrastructure_data.region_id,
        category=infrastructure_data.category,
        infrastructure_type=infrastructure_data.infrastructure_type,
        name=infrastructure_data.name,
        capacity=infrastructure_data.capacity,
        coverage_percent=infrastructure_data.coverage_percent,
        quality_score=infrastructure_data.quality_score,
        operational=infrastructure_data.operational,
        latitude=infrastructure_data.latitude,
        longitude=infrastructure_data.longitude,
    )

    db.add(infrastructure)
    db.commit()
    db.refresh(infrastructure)

    return infrastructure