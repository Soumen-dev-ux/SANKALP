from app.schemas.ai_understanding import StructuredCitizenUnderstanding
from app.services.ai.base import (
    CitizenLocation,
    CitizenUnderstanding,
)


def normalize_understanding(
    result: StructuredCitizenUnderstanding,
) -> CitizenUnderstanding:

    location = CitizenLocation(
        text=result.location.text,
        location_type=result.location.type,
        name=result.location.name,
        ward=result.location.ward,
        district=result.location.district,
        landmark=result.location.landmark,
    )

    return CitizenUnderstanding(
        language=result.language,
        category=result.category,
        intent=result.intent,
        issue=result.issue,
        location=location,
        confidence=getattr(result, "confidence", None),
    )