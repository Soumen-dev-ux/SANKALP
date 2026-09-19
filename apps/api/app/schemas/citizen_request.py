from datetime import datetime

from pydantic import BaseModel, Field

from typing import  Literal


class CitizenRequestCreate(BaseModel):
    raw_text: str = Field(
        ...,
        min_length=3,
        max_length=5000
    )

    language: str | None = Field(
        default=None,
        max_length=20
    )

    category: str | None = Field(
        default=None,
        max_length=100
    )

    intent: str | None = Field(
        default=None,
        max_length=100
    )

    issue: str | None = Field(
        default=None,
        max_length=255
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180
    )

    source: Literal["web", "voice"] = "web"


class CitizenRequestResponse(BaseModel):
    id: int
    anonymous_reference: str
    raw_text: str

    language: str | None
    category: str | None
    intent: str | None
    issue: str | None

    region_id: int | None

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180
    )

    status: str
    source: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }