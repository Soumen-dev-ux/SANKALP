from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.infrastructure_gap import (
    RegionalInfrastructureGapResponse,
)
from app.services.infrastructure_gap_service import (
    get_infrastructure_gap,
)


router = APIRouter(
    prefix="/infrastructure-gap",
    tags=["Infrastructure Intelligence"],
)


@router.get(
    "/regions/{region_id}",
    response_model=RegionalInfrastructureGapResponse,
)
def regional_infrastructure_gap(
    region_id: int,
    db: Session = Depends(get_db),
):
    result = get_infrastructure_gap(
        db,
        region_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return result