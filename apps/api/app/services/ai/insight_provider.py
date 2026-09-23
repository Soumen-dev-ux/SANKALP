from functools import lru_cache

from app.core.config import settings
from app.services.insight_explaination_service import (
    build_deterministic_explanation,
)
@lru_cache
def get_insight_explanation_provider():

    if settings.ai_provider.lower() == "openai":
        from app.services.ai.openai_insight_explaination import (
            OpenAIInsightExplanationProvider,
        )

        return OpenAIInsightExplanationProvider()

    return DeterministicInsightExplanationProvider()


class DeterministicInsightExplanationProvider:

    def explain_insight(self, insight):
        return build_deterministic_explanation(insight)