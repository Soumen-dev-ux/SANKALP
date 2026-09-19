from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


ProjectStatus = Literal[
    "Planned",
    "Ongoing",
    "Completed",
    "Cancelled",
]


class GovernmentProjectCreate(BaseModel):

    region_id: int

    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    category: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    description: str | None = None

    status: ProjectStatus

    budget: float | None = Field(
        default=None,
        ge=0,
    )

    implementing_agency: str | None = Field(
        default=None,
        max_length=255,
    )

    start_date: datetime | None = None

    expected_completion_date: datetime | None = None

    actual_completion_date: datetime | None = None

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


class GovernmentProjectResponse(BaseModel):

    id: int
    region_id: int

    name: str
    category: str
    description: str | None

    status: ProjectStatus

    budget: float | None
    implementing_agency: str | None

    start_date: datetime | None
    expected_completion_date: datetime | None
    actual_completion_date: datetime | None

    latitude: float | None
    longitude: float | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }