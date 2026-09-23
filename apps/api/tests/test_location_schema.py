import pytest
from pydantic import ValidationError

from app.schemas.location import LocationEntity


def test_valid_location():
    location = LocationEntity(
        text="Boral village",
        type="village",
        name="Boral",
    )

    assert location.name == "Boral"


def test_invalid_coordinates_are_not_part_of_ai_location():
    location = LocationEntity(
        text="Boral",
        type="village",
        name="Boral",
    )

    assert not hasattr(location, "latitude")
    assert not hasattr(location, "longitude")