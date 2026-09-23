import pytest
from pydantic import ValidationError

from app.schemas.ai_understanding import (
    StructuredCitizenUnderstanding,
)


from app.schemas.location import LocationEntity


def test_valid_understanding():
    result = StructuredCitizenUnderstanding(
        language="en",
        category="Healthcare",
        intent="Report Development Need",
        issue="Lack of healthcare facility",
        location=LocationEntity(text="in our village"),
    )

    assert result.language == "en"
    assert result.category == "Healthcare"


def test_invalid_language():
    with pytest.raises(ValidationError):
        StructuredCitizenUnderstanding(
            language="english",
            category="Healthcare",
            intent="Report Development Need",
            issue="Lack of healthcare facility",
            location=LocationEntity(),
        )


def test_invalid_category():
    with pytest.raises(ValidationError):
        StructuredCitizenUnderstanding(
            language="en",
            category="Hospital Construction",
            intent="Report Development Need",
            issue="Lack of healthcare facility",
            location=LocationEntity(),
        )


def test_location_can_be_missing():
    result = StructuredCitizenUnderstanding(
        language="en",
        category="Education",
        intent="Report Development Need",
        issue="No nearby school",
        location=LocationEntity(text=None),
    )

    assert result.location.text is None