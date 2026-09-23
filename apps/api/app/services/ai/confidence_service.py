from app.schemas.confidence import UnderstandingConfidence


def calculate_overall_confidence(
    confidence: UnderstandingConfidence,
) -> float:
    scores = [
        confidence.language.score,
        confidence.category.score,
        confidence.intent.score,
        confidence.issue.score,
        confidence.location.score,
    ]

    return round(sum(scores) / len(scores), 2)


def requires_review(
    confidence: UnderstandingConfidence,
) -> bool:
    return (
        confidence.overall_score < 0.70
        or confidence.language.score < 0.50
        or confidence.category.score < 0.50
        or confidence.issue.score < 0.50
        or confidence.location.score < 0.40
    )