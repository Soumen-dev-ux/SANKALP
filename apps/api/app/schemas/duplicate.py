from pydantic import BaseModel, Field


class DuplicateCandidate(BaseModel):
    request_id: int
    anonymous_reference: str
    category: str | None
    similarity_score: float = Field(
        ge=0,
        le=1,
    )
    match_level: str
    reason: str


class DuplicateCheckResponse(BaseModel):
    is_potential_duplicate: bool
    candidates: list[DuplicateCandidate]