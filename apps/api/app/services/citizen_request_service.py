import uuid

from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.schemas.citizen_request import CitizenRequestCreate


def create_citizen_request(
    db: Session,
    request_data: CitizenRequestCreate,
) -> CitizenRequest:

    anonymous_reference = (
        f"SANKALP-{uuid.uuid4().hex[:10].upper()}"
    )

    request = CitizenRequest(
        anonymous_reference=anonymous_reference,
        raw_text=request_data.raw_text,
        language=request_data.language or "en",
        category=request_data.category,
        intent=request_data.intent,
        issue=request_data.issue,
        region_id=getattr(request_data, "region_id", None),
        latitude=request_data.latitude,
        longitude=request_data.longitude,
        source=request_data.source,
        status="submitted",
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return request
