import json

try:
    # pyrefly: ignore [missing-import]
    from openai import OpenAI
except ImportError:
    OpenAI = None

from app.core.config import settings
from app.schemas.insight_explaination import (
    InsightExplanationRequest,
    InsightExplanationResponse,
)


class OpenAIInsightExplanationProvider:
    def __init__(self):
        if not settings.ai_api_key:
            raise ValueError("AI_API_KEY is not configured")

        self.client = OpenAI(api_key=settings.ai_api_key)

    def explain_insight(
        self,
        insight: InsightExplanationRequest,
    ) -> InsightExplanationResponse:

        payload = {
            "region_name": insight.region_name,
            "category": insight.category,
            "request_count": insight.request_count,
            "demand_score": insight.demand_score,
            "infrastructure_coverage": insight.infrastructure_coverage,
            "infrastructure_quality": insight.infrastructure_quality,
            "gap_score": insight.gap_score,
            "project_count": insight.project_count,
            "project_coverage": insight.project_coverage,
            "population": insight.population,
            "population_density": insight.population_density,
            "evidence": insight.evidence,
            "data_warnings": insight.data_warnings,
        }

        system_prompt = """
You are the explanation layer of SANKALP.

Your job is ONLY to explain already-computed development analytics.

Strict rules:

1. Use only the supplied data.
2. Do not calculate or modify scores.
3. Do not create new facts.
4. Do not invent infrastructure, projects, budgets, populations,
   locations, or citizen requests.
5. Do not recommend a policy, project, budget, or government action.
6. Do not rank regions or categories.
7. Do not claim that an existing project solved an issue.
8. Treat missing data as a limitation.
9. Evidence must be referenced only by its supplied index.
10. Return valid JSON only.

Return:

{
  "summary": "short human-readable explanation",
  "evidence_references": [0, 1],
  "limitation_references": [0],
  "review_note": "short human-review note"
}

Do not include new numeric facts in the summary.
"""

        response = self.client.chat.completions.create(
            model=settings.ai_model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(payload),
                },
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("AI returned an empty explanation")

        result = json.loads(content)

        return InsightExplanationResponse.model_validate(result)