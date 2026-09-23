import re
from difflib import SequenceMatcher

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.schemas.duplicate import (
    DuplicateCandidate,
    DuplicateCheckResponse,
)


STOP_WORDS = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "there",
    "our",
    "in",
    "of",
    "to",
    "for",
    "and",
    "with",
    "has",
    "have",
    "no",
    "not",
}


def normalize_text(text: str) -> str:
    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
        flags=re.UNICODE,
    )

    words = [
        word
        for word in text.split()
        if word not in STOP_WORDS
    ]

    return " ".join(words)


def text_similarity(
    first: str,
    second: str,
) -> float:
    first_normalized = normalize_text(first)
    second_normalized = normalize_text(second)

    if not first_normalized or not second_normalized:
        return 0.0

    return round(
        SequenceMatcher(
            None,
            first_normalized,
            second_normalized,
        ).ratio(),
        2,
    )

def coordinates_are_nearby(
    latitude_a: float | None,
    longitude_a: float | None,
    latitude_b: float | None,
    longitude_b: float | None,
    threshold: float = 0.02,
) -> bool:
    if (
        latitude_a is None
        or longitude_a is None
        or latitude_b is None
        or longitude_b is None
    ):
        return False

    return (
        abs(latitude_a - latitude_b) <= threshold
        and abs(longitude_a - longitude_b) <= threshold
    )

def get_match_level(score: float) -> str:
    if score >= 0.85:
        return "high"

    if score >= 0.65:
        return "medium"

    return "low"

def check_for_duplicates(
    db: Session,
    text: str,
    category: str | None = None,
    region_id: int | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    limit: int = 10,
) -> DuplicateCheckResponse:

    query = select(CitizenRequest)

    if region_id is not None:
        query = query.where(
            CitizenRequest.region_id == region_id
        )

    if category:
        query = query.where(
            CitizenRequest.category == category
        )

    query = query.order_by(
        CitizenRequest.created_at.desc()
    ).limit(100)

    existing_requests = db.scalars(query).all()

    candidates: list[DuplicateCandidate] = []

    for request in existing_requests:

        similarity = text_similarity(
            text,
            request.raw_text,
        )

        nearby = coordinates_are_nearby(
            latitude,
            longitude,
            request.latitude,
            request.longitude,
        )

        same_region = (
            region_id is not None
            and request.region_id == region_id
        )

        if nearby:
            similarity = min(
                1.0,
                similarity + 0.10,
            )

        elif same_region:
            similarity = min(
                1.0,
                similarity + 0.05,
            )

        if similarity < 0.65:
            continue

        match_level = get_match_level(similarity)

        if nearby:
            reason = (
                "Very similar development issue "
                "in a nearby location."
            )
        elif same_region:
            reason = (
                "Similar development issue "
                "in the same region."
            )
        else:
            reason = (
                "Very similar wording and "
                "development issue."
            )

        candidates.append(
            DuplicateCandidate(
                request_id=request.id,
                anonymous_reference=request.anonymous_reference,
                category=request.category,
                similarity_score=similarity,
                match_level=match_level,
                reason=reason,
            )
        )

    candidates.sort(
        key=lambda item: item.similarity_score,
        reverse=True,
    )

    candidates = candidates[:limit]

    return DuplicateCheckResponse(
        is_potential_duplicate=any(
            candidate.match_level == "high"
            for candidate in candidates
        ),
        candidates=candidates,
    )