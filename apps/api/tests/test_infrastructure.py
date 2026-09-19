from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.infrastructure import (
    InfrastructureCreate,
    InfrastructureResponse,
)

from app.services.infrastructure_service import (
    create_infrastructure,
)


router = APIRouter(
    prefix="/infrastructure",
    tags=["Infrastructure"],
)


@router.post(
    "",
    response_model=InfrastructureResponse,
)
def create_infrastructure_record(
    infrastructure_data: InfrastructureCreate,
    db: Session = Depends(get_db),
):

    return create_infrastructure(
        db,
        infrastructure_data,
    )