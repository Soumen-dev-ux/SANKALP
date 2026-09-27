from fastapi import APIRouter
from app.schemas.insight_explaination import (
    InsightExplanationRequest,
    InsightExplanationResponse,
)
from app.services.insight_explaination_service import (
    build_deterministic_explanation,
)

from fastapi import APIRouter, Depends
from app.api.dependencies.rbac import require_roles

router = APIRouter(
    prefix="/insight-explanations",
    tags=["Insight Explanations"],
    dependencies=[
        Depends(
            require_roles(
                "admin",
                "reviewer",
                "analyst",
                "viewer",
            )
        )
    ],
)


@router.post(
    "/explain",
    response_model=InsightExplanationResponse,
)
def explain_insight_endpoint(
    payload: InsightExplanationRequest,
):
    return build_deterministic_explanation(payload)
