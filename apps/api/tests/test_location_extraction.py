from app.services.ai.provider import get_ai_provider


def test_generic_village_location():
    provider = get_ai_provider()

    result = provider.understand(
        "There is no drinking water facility in our village."
    )

    assert result.location.location_type == "village"
    assert result.location.name is None


def test_generic_area_location():
    provider = get_ai_provider()

    result = provider.understand(
        "There is no proper road in our area."
    )

    assert result.location.location_type == "area"


def test_location_is_optional():
    provider = get_ai_provider()

    result = provider.understand(
        "There is no proper drinking water facility."
    )

    assert result.location.location_type == "unknown"
    assert result.location.name is None