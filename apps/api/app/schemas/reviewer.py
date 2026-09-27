from datetime import datetime

from pydantic import BaseModel


class PendingReviewResponse(BaseModel):
    request_id: int
    anonymous_reference: str
    raw_text: str
    category: str | None
    issue: str | None
    location_text: str | None
    confidence_review_required: bool
    review_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ReviewActionResponse(BaseModel):
    id: int
    request_id: int
    reviewer_id: int
    status: str
    reviewer_note: str | None
    reviewed_category: str | None
    reviewed_issue: str | None
    reviewed_location: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }