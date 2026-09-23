from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.schemas.human_review import HumanReviewCreate


def submit_human_review(
    db: Session,
    request_id: int,
    review: HumanReviewCreate,
) -> CitizenRequest:

    request = (
        db.query(CitizenRequest)
        .filter(CitizenRequest.id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Citizen request not found",
        )

    if review.status == "corrected":
        if not any(
            [
                review.reviewed_category,
                review.reviewed_issue,
                review.reviewed_location,
            ]
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    "At least one corrected field is required "
                    "when review status is corrected"
                ),
            )

    request.review_status = review.status
    request.reviewer_note = review.reviewer_note
    request.reviewed_category = review.reviewed_category
    request.reviewed_issue = review.reviewed_issue
    request.reviewed_location = review.reviewed_location
    request.reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(request)

    return request