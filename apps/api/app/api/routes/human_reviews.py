from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.human_review import (
    HumanReviewCreate,
    HumanReviewResponse,
)
from app.services.ai.human_review_service import submit_human_review


router = APIRouter(
    prefix="/requests",
    tags=["Human Review"],
)


@router.post(
    "/{request_id}/review",
    response_model=HumanReviewResponse,
)
def review_request(
    request_id: int,
    review: HumanReviewCreate,
    db: Session = Depends(get_db),
):
    return submit_human_review(
        db=db,
        request_id=request_id,
        review=review,
    )