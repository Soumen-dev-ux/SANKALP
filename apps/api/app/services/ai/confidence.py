from app.schemas.confidence import FieldConfidence


def confidence_level(score: float) -> str:
    if score >= 0.80:
        return "high"

    if score >= 0.50:
        return "medium"

    return "low"


def make_confidence(
    score: float,
    reason: str | None = None,
) -> FieldConfidence:
    score = max(0.0, min(1.0, score))

    return FieldConfidence(
        score=round(score, 2),
        level=confidence_level(score),
        reason=reason,
    )