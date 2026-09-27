import uuid

from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.models.audit_log import AuditLog
from app.schemas.citizen_request import CitizenRequestCreate
from app.services.ai.ai_analysis_service import analyze_citizen_text


def create_citizen_request(
    db: Session,
    request_data: CitizenRequestCreate,
) -> CitizenRequest:

    anonymous_reference = (
        f"SANKALP-{uuid.uuid4().hex[:10].upper()}"
    )

    analysis = analyze_citizen_text(request_data.raw_text)

    review_status = "not_required"
    if analysis and hasattr(analysis, "confidence") and analysis.confidence:
        review_status = (
            "pending"
            if analysis.confidence.review_required
            else "not_required"
        )

    request = CitizenRequest(
        anonymous_reference=anonymous_reference,
        raw_text=request_data.raw_text,
        language=request_data.language or getattr(analysis, "language", None) or "en",
        category=request_data.category or getattr(analysis, "category", None),
        intent=request_data.intent or getattr(analysis, "intent", None),
        issue=request_data.issue or getattr(analysis, "issue", None),
        region_id=getattr(request_data, "region_id", None),
        latitude=request_data.latitude,
        longitude=request_data.longitude,
        source=request_data.source,
        status="submitted",
        review_status=review_status,
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    audit_log = AuditLog(
        user_id=None,
        action="CREATE_REQUEST",
        resource_type="citizen_request",
        resource_id=str(request.id),
        metadata={"anonymous_reference": anonymous_reference}
    )
    db.add(audit_log)
    db.commit()

    return request
