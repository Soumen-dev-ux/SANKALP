from app.services.ai.base import CitizenUnderstanding
from app.services.ai.mock_provider import MockAIProvider

ai_provider = MockAIProvider()

def analyze_citizen_text(
    text: str,
) -> CitizenUnderstanding:
    return ai_provider.understand(text)