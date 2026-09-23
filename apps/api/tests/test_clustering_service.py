from app.services.clustering_service import (
    cosine_similarity,
    tokenize,
)


def test_tokenize():
    result = tokenize(
        "There is no proper drinking water facility."
    )

    assert "drinking" in result
    assert "water" in result
    assert "the" not in result


def test_identical_vectors():
    result = cosine_similarity(
        [1.0, 2.0, 3.0],
        [1.0, 2.0, 3.0],
    )

    assert result == 1.0


def test_different_vectors():
    result = cosine_similarity(
        [1.0, 0.0],
        [0.0, 1.0],
    )

    assert result == 0.0