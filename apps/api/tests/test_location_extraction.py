from app.services.ai.mock_provider import MockAIProvider


provider = MockAIProvider()


def test_english_location():

    result = provider.extract_location(
        "There is no drinking water in our village"
    )

    assert result == "in our village"


def test_bengali_location():

    result = provider.extract_location(
        "আমাদের এলাকায় পানীয় জলের সমস্যা হচ্ছে"
    )

    assert result == "আমাদের এলাকায়"


def test_hindi_location():

    result = provider.extract_location(
        "हमारे इलाके में पीने के पानी की समस्या है"
    )

    assert result == "हमारे इलाके में"


def test_no_location():

    result = provider.extract_location(
        "The hospital needs better facilities"
    )

    assert result is None