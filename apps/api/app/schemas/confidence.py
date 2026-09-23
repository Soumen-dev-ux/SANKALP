from pydantic import BaseModel, Field


class FieldConfidence(BaseModel):
    score: float = Field(
        ge=0,
        le=1,
    )

    level: str

    reason: str | None = None


class UnderstandingConfidence(BaseModel):
    language: FieldConfidence
    category: FieldConfidence
    intent: FieldConfidence
    issue: FieldConfidence
    location: FieldConfidence

    overall_score: float = Field(
        ge=0,
        le=1,
    )

    review_required: bool