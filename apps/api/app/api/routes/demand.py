from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.demand import RegionalDemandResponse
from app.services.demand_service import (
    get_regional_demand,
)


router = APIRouter(
    prefix="/demand",
    tags=["Demand Intelligence"],
)


@router.get(
    "/regions/{region_id}",
    response_model=RegionalDemandResponse,
)
def regional_demand(
    region_id: int,
    db: Session = Depends(get_db),
):
    result = get_regional_demand(
        db,
        region_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return result