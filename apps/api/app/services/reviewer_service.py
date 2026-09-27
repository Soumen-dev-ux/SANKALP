from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.models.human_review_action import HumanReviewAction
from app.models.audit_log import AuditLog
from app.models.user import User
from app.schemas.human_review import HumanReviewCreate


def get_pending_reviews(db: Session):
    return (
        db.query(CitizenRequest)
        .filter(
            CitizenRequest.review_status == "pending"
        )
        .order_by(CitizenRequest.created_at.asc())
        .all()
    )


def create_review_action(
    db: Session,
    request_id: int,
    reviewer: User,
    payload: HumanReviewCreate,
):
    request = (
        db.query(CitizenRequest)
        .filter(CitizenRequest.id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citizen request not found",
        )

    if request.review_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This request is not currently pending review",
        )

    if payload.status == "corrected":
        if not any(
            [
                payload.reviewed_category,
                payload.reviewed_issue,
                payload.reviewed_location,
            ]
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one corrected field is required",
            )

    action = HumanReviewAction(
        request_id=request.id,
        reviewer_id=reviewer.id,
        status=payload.status,
        reviewer_note=payload.reviewer_note,
        reviewed_category=payload.reviewed_category,
        reviewed_issue=payload.reviewed_issue,
        reviewed_location=payload.reviewed_location,
        created_at=datetime.now(timezone.utc),
    )

    db.add(action)

    request.review_status = payload.status
    request.reviewer_note = payload.reviewer_note
    request.reviewed_at = datetime.now(timezone.utc)

    if payload.reviewed_category is not None:
        request.reviewed_category = payload.reviewed_category

    if payload.reviewed_issue is not None:
        request.reviewed_issue = payload.reviewed_issue

    if payload.reviewed_location is not None:
        request.reviewed_location = payload.reviewed_location

    audit_action = "REVIEW_CORRECTED" if payload.status == "corrected" else "REVIEW_APPROVED"
    audit_log = AuditLog(
        user_id=reviewer.id,
        action=audit_action,
        resource_type="citizen_request",
        resource_id=str(request.id),
        meta_data={"reviewer_note": payload.reviewer_note} if payload.reviewer_note else None
    )
    db.add(audit_log)

    db.commit()
    db.refresh(action)

    return action


def get_request_review_history(
    db: Session,
    request_id: int,
):
    request = (
        db.query(CitizenRequest)
        .filter(CitizenRequest.id == request_id)
        .first()
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citizen request not found",
        )

    return (
        db.query(HumanReviewAction)
        .filter(
            HumanReviewAction.request_id == request_id
        )
        .order_by(HumanReviewAction.created_at.desc())
        .all()
    )