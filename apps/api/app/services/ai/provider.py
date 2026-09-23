from functools import lru_cache

from app.core.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.mock_provider import MockAIProvider
@lru_cache
def get_ai_provider() -> AIProvider:
    provider_name = settings.ai_provider.lower()

    if provider_name == "mock":
        return MockAIProvider()

    if provider_name == "openai":
        from app.services.ai.openai_provider import OpenAIProvider

        return OpenAIProvider()

    raise ValueError(
        f"Unsupported AI provider: {settings.ai_provider}"
    )

def analyze_citizen_request(text: str):
    provider = get_ai_provider()
    return provider.understand(text)