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


router = APIRouter(
    prefix="/demographics",
    tags=["Demographics"],
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
