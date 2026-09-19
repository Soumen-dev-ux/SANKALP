from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.region import (
    RegionResponse,
    RegionSummaryResponse,
)
from app.services.region_service import (
    get_regions,
    get_region,
    get_region_demographics,
    get_region_infrastructure,
    get_region_projects,
    get_region_requests,
    get_region_summary,
)


router = APIRouter(
    prefix="/regions",
    tags=["Regions"],
)


@router.get(
    "",
    response_model=list[RegionResponse],
)
def list_regions(
    db: Session = Depends(get_db),
):
    return get_regions(db)


@router.get(
    "/{region_id}",
    response_model=RegionResponse,
)
def retrieve_region(
    region_id: int,
    db: Session = Depends(get_db),
):
    region = get_region(db, region_id)

    if not region:
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return region


@router.get(
    "/{region_id}/summary",
    response_model=RegionSummaryResponse,
)
def retrieve_region_summary(
    region_id: int,
    db: Session = Depends(get_db),
):
    summary = get_region_summary(
        db,
        region_id,
    )

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return summary


@router.get(
    "/{region_id}/demographics",
)
def retrieve_region_demographics(
    region_id: int,
    db: Session = Depends(get_db),
):
    if not get_region(db, region_id):
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return get_region_demographics(
        db,
        region_id,
    )


@router.get(
    "/{region_id}/infrastructure",
)
def retrieve_region_infrastructure(
    region_id: int,
    db: Session = Depends(get_db),
):
    if not get_region(db, region_id):
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return get_region_infrastructure(
        db,
        region_id,
    )


@router.get(
    "/{region_id}/projects",
)
def retrieve_region_projects(
    region_id: int,
    db: Session = Depends(get_db),
):
    if not get_region(db, region_id):
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return get_region_projects(
        db,
        region_id,
    )


@router.get(
    "/{region_id}/requests",
)
def retrieve_region_requests(
    region_id: int,
    db: Session = Depends(get_db),
):
    if not get_region(db, region_id):
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return get_region_requests(
        db,
        region_id,
    )