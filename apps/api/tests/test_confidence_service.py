from app.schemas.confidence import (
    FieldConfidence,
    UnderstandingConfidence,
)

from app.services.ai.confidence_service import (
    calculate_overall_confidence,
    requires_review,
)


def test_overall_confidence():

    confidence = UnderstandingConfidence(
        language=FieldConfidence(
            score=0.9,
            level="high",
        ),
        category=FieldConfidence(
            score=0.9,
            level="high",
        ),
        intent=FieldConfidence(
            score=0.8,
            level="high",
        ),
        issue=FieldConfidence(
            score=0.9,
            level="high",
        ),
        location=FieldConfidence(
            score=0.8,
            level="high",
        ),
        overall_score=0.86,
        review_required=False,
    )

    result = calculate_overall_confidence(confidence)

    assert result == 0.86


def test_low_confidence_requires_review():

    confidence = UnderstandingConfidence(
        language=FieldConfidence(
            score=0.9,
            level="high",
        ),
        category=FieldConfidence(
            score=0.4,
            level="low",
        ),
        intent=FieldConfidence(
            score=0.8,
            level="high",
        ),
        issue=FieldConfidence(
            score=0.4,
            level="low",
        ),
        location=FieldConfidence(
            score=0.2,
            level="low",
        ),
        overall_score=0.54,
        review_required=True,
    )

    assert requires_review(confidence) is True