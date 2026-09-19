from datetime import datetime

from pydantic import BaseModel, Field


class DemographicCreate(BaseModel):

    region_id: int

    population: int = Field(
        ...,
        ge=0,
    )

    population_density: float | None = Field(
        default=None,
        ge=0,
    )

    income_index: float | None = Field(
        default=None,
        ge=0,
    )

    age_0_14_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    age_15_24_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    age_25_64_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    age_65_plus_percent: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    growth_rate: float | None = None


class DemographicResponse(BaseModel):

    id: int
    region_id: int

    population: int

    population_density: float | None
    income_index: float | None

    age_0_14_percent: float | None
    age_15_24_percent: float | None
    age_25_64_percent: float | None
    age_65_plus_percent: float | None

    growth_rate: float | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }