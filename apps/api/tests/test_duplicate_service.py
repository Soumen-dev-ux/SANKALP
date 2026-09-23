from app.services.duplicate_service import (
    get_match_level,
    normalize_text,
    text_similarity,
)


def test_normalize_text():
    result = normalize_text(
        "There is no proper drinking water facility!"
    )

    assert "drinking" in result
    assert "water" in result
    assert "the" not in result


def test_identical_text_has_high_similarity():
    score = text_similarity(
        "No drinking water facility in our village",
        "No drinking water facility in our village",
    )

    assert score == 1.0


def test_similar_text():
    score = text_similarity(
        "No drinking water facility in our village",
        "There is no drinking water facility in our village",
    )

    assert score >= 0.65


def test_different_text():
    score = text_similarity(
        "No drinking water facility",
        "The road is badly damaged",
    )

    assert score < 0.65


def test_match_levels():
    assert get_match_level(0.90) == "high"
    assert get_match_level(0.70) == "medium"
    assert get_match_level(0.30) == "low"