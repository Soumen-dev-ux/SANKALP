from datetime import datetime

from pydantic import BaseModel, Field


class InfrastructureCreate(BaseModel):

    region_id: int

    category: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    infrastructure_type: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    name: str | None = Field(
        default=None,
        max_length=255,
    )

    capacity: int | None = Field(
        default=None,
        ge=0,
    )

    coverage_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    quality_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    operational: bool = True

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )


class InfrastructureResponse(BaseModel):

    id: int
    region_id: int

    category: str
    infrastructure_type: str
    name: str | None

    capacity: int | None
    coverage_percent: float | None
    quality_score: float | None

    operational: bool

    latitude: float | None
    longitude: float | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }