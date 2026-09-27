from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.development_insight import (
    RegionalDevelopmentInsightResponse,
)
from app.services.development_insight_service import (
    get_development_insights,
)
from app.api.dependencies.rbac import require_roles
from app.models.user import User


router = APIRouter(
    prefix="/development-insights",
    tags=["Development Intelligence"],
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


@router.get(
    "/regions/{region_id}",
    response_model=RegionalDevelopmentInsightResponse,
)
def regional_development_insights(
    region_id: int,
    db: Session = Depends(get_db),
):
    result = get_development_insights(
        db,
        region_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Region not found",
        )

    return result