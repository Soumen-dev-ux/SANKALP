from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.confidence import UnderstandingConfidence
from app.schemas.location import LocationEntity


LanguageCode = Literal["en", "bn", "hi", "other"]

Category = Literal[
    "Healthcare",
    "Transport",
    "Water & Sanitation",
    "Education",
    "Digital Connectivity",
    "Other",
]


class StructuredCitizenUnderstanding(BaseModel):
    language: LanguageCode

    category: Category

    intent: str = Field(
        min_length=1,
        max_length=200,
    )

    issue: str = Field(
        min_length=1,
        max_length=255,
    )

    location: LocationEntity

    confidence: UnderstandingConfidence