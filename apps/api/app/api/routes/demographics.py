from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.demographic import (
    DemographicCreate,
    DemographicResponse,
)

from app.services.demographic_service import (
    create_demographic,
)


from app.api.dependencies.rbac import require_roles

router = APIRouter(
    prefix="/demographics",
    tags=["Demographics"],
    dependencies=[
        Depends(
            require_roles("admin", "reviewer")
        )
    ],
)


@router.post(
    "",
    response_model=DemographicResponse,
)
def create_demographic_record(
    demographic_data: DemographicCreate,
    db: Session = Depends(get_db),
):

    return create_demographic(
        db,
        demographic_data,
    )
