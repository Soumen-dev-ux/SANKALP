from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ReviewStatus = Literal[
    "not_required",
    "pending",
    "approved",
    "corrected",
]


class HumanReviewCreate(BaseModel):
    status: Literal["approved", "corrected"]
    reviewer_note: str | None = Field(
        default=None,
        max_length=2000,
    )

    reviewed_category: str | None = Field(
        default=None,
        max_length=100,
    )

    reviewed_issue: str | None = Field(
        default=None,
        max_length=255,
    )

    reviewed_location: str | None = Field(
        default=None,
        max_length=500,
    )


class HumanReviewResponse(BaseModel):
    request_id: int
    review_status: ReviewStatus
    reviewer_note: str | None
    reviewed_category: str | None
    reviewed_issue: str | None
    reviewed_location: str | None
    reviewed_at: datetime | None

    model_config = {
        "from_attributes": True,
    }