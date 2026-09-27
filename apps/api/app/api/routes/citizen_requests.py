from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.rate_limit import limiter

from app.db.session import get_db
from app.models.citizen_request import CitizenRequest

from app.schemas.citizen_request import (
    CitizenRequestCreate,
    CitizenRequestResponse,
)

from app.schemas.ai_analysis import (
    CitizenAnalysisRequest,
    CitizenAnalysisResponse,
)

from app.services.citizen_request_service import (
    create_citizen_request,
)

from app.services.ai.ai_analysis_service import (
    analyze_citizen_text,
)

from app.schemas.duplicate import DuplicateCheckResponse
from app.services.duplicate_service import check_for_duplicates


router = APIRouter(
    prefix="/requests",
    tags=["Citizen Requests"],
)


@router.post(
    "",
    response_model=CitizenRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def submit_citizen_request(
    request: Request,
    request_data: CitizenRequestCreate,
    db: Session = Depends(get_db),
):

    return create_citizen_request(
        db,
        request_data,
    )


@router.post(
    "/analyze",
    response_model=CitizenAnalysisResponse,
)
@limiter.limit("20/minute")
def analyze_request(
    request: Request,
    request_data: CitizenAnalysisRequest,
):

    result = analyze_citizen_text(
        request_data.text
    )

    return result


@router.get(
    "/{request_id}",
    response_model=CitizenRequestResponse,
)
def get_citizen_request(
    request_id: int,
    db: Session = Depends(get_db),
):

    request = (
        db.query(CitizenRequest)
        .filter(
            CitizenRequest.id == request_id
        )
        .first()
    )

    if not request:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citizen request not found",
        )

    return request

@router.post(
    "/duplicate-check",
    response_model=DuplicateCheckResponse,
)
@limiter.limit("20/minute")
def duplicate_check(
    request: Request,
    payload: CitizenRequestCreate,
    db: Session = Depends(get_db),
):
    return check_for_duplicates(
        db=db,
        text=payload.raw_text,
        category=payload.category,
        region_id=payload.region_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )