from app.services.ai.mock_provider import MockAIProvider


provider = MockAIProvider()


def test_english_water_request():

    result = provider.understand(
        "There is no drinking water in our village"
    )

    assert result.language == "en"
    assert result.category == "Water & Sanitation"
    assert result.issue == "Drinking Water"


def test_bengali_water_request():

    result = provider.understand(
        "আমাদের এলাকায় পানীয় জলের সমস্যা হচ্ছে"
    )

    assert result.language == "bn"
    assert result.category == "Water & Sanitation"
    assert result.issue == "Drinking Water"


def test_hindi_water_request():

    result = provider.understand(
        "हमारे इलाके में पीने के पानी की समस्या है"
    )

    assert result.language == "hi"
    assert result.category == "Water & Sanitation"
    assert result.issue == "Drinking Water"


def test_healthcare_request():

    result = provider.understand(
        "There is no hospital near our village"
    )

    assert result.category == "Healthcare"
    assert result.issue == "Healthcare Facility"


def test_transport_request():

    result = provider.understand(
        "Our road has severe traffic problems"
    )

    assert result.category == "Transport"


def test_education_request():

    result = provider.understand(
        "Our school needs more teachers"
    )

    assert result.category == "Education"


def test_digital_connectivity_request():

    result = provider.understand(
        "There is no internet connectivity here"
    )

    assert result.category == "Digital Connectivity"