from typing import Literal

from pydantic import BaseModel, Field


LocationType = Literal[
    "village",
    "town",
    "city",
    "ward",
    "district",
    "locality",
    "landmark",
    "area",
    "unknown",
]


class LocationEntity(BaseModel):
    text: str | None = Field(
        default=None,
        max_length=500,
    )

    type: LocationType = "unknown"

    name: str | None = Field(
        default=None,
        max_length=255,
    )

    ward: str | None = Field(
        default=None,
        max_length=255,
    )

    district: str | None = Field(
        default=None,
        max_length=255,
    )

    landmark: str | None = Field(
        default=None,
        max_length=255,
    )


class LocationCoordinates(BaseModel):
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