from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.government_projects import (
    GovernmentProjectCreate,
    GovernmentProjectResponse,
)

from app.services.government_project_service import (
    create_government_project,
)


router = APIRouter(
    prefix="/government-projects",
    tags=["Government Projects"],
)


@router.post(
    "",
    response_model=GovernmentProjectResponse,
)
def create_project(
    project_data: GovernmentProjectCreate,
    db: Session = Depends(get_db),
):

    return create_government_project(
        db,
        project_data,
    )