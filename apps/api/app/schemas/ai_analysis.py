from unicodedata import category
from pydantic import BaseModel, Field

class CitizenAnalysisRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=3,
        max_length=5000
    )

class CitizenAnalysisResponse(BaseModel):
    language: str | None
    category: str | None
    intent: str | None
    issue: str | None
    location_text: str | None