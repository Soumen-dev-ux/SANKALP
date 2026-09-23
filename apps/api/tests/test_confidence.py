import pytest

from app.services.ai.confidence import (
    confidence_level,
    make_confidence,
)


def test_high_confidence():
    result = make_confidence(0.90)

    assert result.score == 0.90
    assert result.level == "high"


def test_medium_confidence():
    result = make_confidence(0.65)

    assert result.score == 0.65
    assert result.level == "medium"


def test_low_confidence():
    result = make_confidence(0.30)

    assert result.score == 0.30
    assert result.level == "low"


def test_score_is_clamped():
    result = make_confidence(1.5)

    assert result.score == 1.0


def test_negative_score_is_clamped():
    result = make_confidence(-0.5)

    assert result.score == 0.0