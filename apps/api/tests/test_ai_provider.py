from app.services.ai.provider import get_ai_provider
from app.services.ai.mock_provider import MockAIProvider


def test_default_ai_provider_is_mock():
    provider = get_ai_provider()

    assert isinstance(provider, MockAIProvider)


def test_mock_provider_understands_request():
    provider = get_ai_provider()

    result = provider.understand(
        "There is no proper drinking water facility in our village."
    )

    assert result.category == "Water & Sanitation"
    assert result.issue == "Drinking Water"
    assert result.intent == "Report Development Need"