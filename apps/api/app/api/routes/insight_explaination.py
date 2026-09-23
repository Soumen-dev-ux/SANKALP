from fastapi import APIRouter
from app.schemas.insight_explaination import (
    InsightExplanationRequest,
    InsightExplanationResponse,
)
from app.services.insight_explaination_service import (
    build_deterministic_explanation,
)

router = APIRouter(
    prefix="/insight-explanations",
    tags=["Insight Explanations"],
)


@router.post(
    "/explain",
    response_model=InsightExplanationResponse,
)
def explain_insight_endpoint(
    payload: InsightExplanationRequest,
):
    return build_deterministic_explanation(payload)
