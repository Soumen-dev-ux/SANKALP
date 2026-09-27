from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.rbac import require_roles
from app.db.session import get_db

from app.models.user import User
from app.schemas.human_review import HumanReviewCreate
from app.schemas.reviewer import (
    PendingReviewResponse,
    ReviewActionResponse,
)
from app.services.reviewer_service import (
    create_review_action,
    get_pending_reviews,
    get_request_review_history,
)

router = APIRouter(
    prefix="/reviews",
    tags=["Human Review"],
)


@router.get(
    "/pending",
    response_model=list[PendingReviewResponse],
)
def pending_reviews(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "reviewer")
    ),
):
    return get_pending_reviews(db)


@router.post(
    "/requests/{request_id}",
    response_model=ReviewActionResponse,
)
def review_request(
    request_id: int,
    payload: HumanReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "reviewer")
    ),
):
    return create_review_action(
        db=db,
        request_id=request_id,
        reviewer=current_user,
        payload=payload,
    )


@router.get(
    "/requests/{request_id}/history",
    response_model=list[ReviewActionResponse],
)
def review_history(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles("admin", "reviewer", "analyst", "viewer")
    ),
):
    return get_request_review_history(
        db=db,
        request_id=request_id,
    )