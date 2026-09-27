from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.clustering import SemanticClusterResponse
from app.services.clustering_service import (
    get_regional_clusters,
)


from app.api.dependencies.rbac import require_roles

router = APIRouter(
    prefix="/clusters",
    tags=["Semantic Clustering"],
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
    response_model=list[SemanticClusterResponse],
)
def get_region_clusters(
    region_id: int,
    db: Session = Depends(get_db),
):
    return get_regional_clusters(
        db=db,
        region_id=region_id,
    )