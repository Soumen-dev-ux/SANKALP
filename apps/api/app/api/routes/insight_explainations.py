from fastapi import APIRouter

from app.schemas.insight_explaination import (
    InsightExplanationRequest,
    InsightExplanationResponse,
)
from app.services.ai.insight_provider import (
    get_insight_explanation_provider,
)


router = APIRouter(
    prefix="/insight-explanations",
    tags=["AI Insight Explanation"],
)


@router.post(
    "",
    response_model=InsightExplanationResponse,
)
@router.post(
    "/",
    response_model=InsightExplanationResponse,
)
def explain_insight(
    insight: InsightExplanationRequest,
):
    provider = get_insight_explanation_provider()

    return provider.explain_insight(insight)