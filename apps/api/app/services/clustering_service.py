import hashlib
import math
import re
from collections import Counter

from app.models.citizen_request import CitizenRequest

from app.schemas.clustering import (
    SemanticClusterResponse,
    SemanticClusterMember,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest


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
    "this",
    "that",
}


def tokenize(text: str) -> list[str]:
    text = text.lower()

    text = re.sub(
        r"[^\w\s]",
        " ",
        text,
        flags=re.UNICODE,
    )

    return [
        word
        for word in text.split()
        if word not in STOP_WORDS
    ]

def build_vocabulary(
    requests: list[CitizenRequest],
) -> list[str]:
    vocabulary: set[str] = set()

    for request in requests:
        vocabulary.update(
            tokenize(request.raw_text)
        )

    return sorted(vocabulary)


def build_vector(
    text: str,
    vocabulary: list[str],
    document_frequency: dict[str, int],
    document_count: int,
) -> list[float]:

    tokens = tokenize(text)
    counts = Counter(tokens)

    vector: list[float] = []

    for word in vocabulary:
        term_frequency = counts[word]

        if term_frequency == 0:
            vector.append(0.0)
            continue

        tf = 1 + math.log(term_frequency)

        df = document_frequency.get(word, 0)

        idf = math.log(
            (document_count + 1)
            / (df + 1)
        ) + 1

        vector.append(tf * idf)

    return vector

def cosine_similarity(
    first: list[float],
    second: list[float],
) -> float:

    dot_product = sum(
        a * b
        for a, b in zip(first, second)
    )

    first_norm = math.sqrt(
        sum(value * value for value in first)
    )

    second_norm = math.sqrt(
        sum(value * value for value in second)
    )

    if first_norm == 0 or second_norm == 0:
        return 0.0

    return round(
        dot_product / (first_norm * second_norm),
        4,
    )

def create_cluster_id(
    request_ids: list[int],
) -> str:

    normalized = ",".join(
        str(request_id)
        for request_id in sorted(request_ids)
    )

    digest = hashlib.sha256(
        normalized.encode()
    ).hexdigest()[:12]

    return f"CLUSTER-{digest.upper()}"

def same_cluster_domain(
    first: CitizenRequest,
    second: CitizenRequest,
) -> bool:
    if first.category and second.category:
        return first.category == second.category
    return True


def cluster_requests(
    requests: list[CitizenRequest],
    similarity_threshold: float = 0.60,
) -> list[SemanticClusterResponse]:

    if not requests:
        return []

    vocabulary = build_vocabulary(requests)

    document_frequency: dict[str, int] = Counter()

    for request in requests:
        unique_tokens = set(
            tokenize(request.raw_text)
        )

        for token in unique_tokens:
            document_frequency[token] += 1

    vectors = {
        request.id: build_vector(
            request.raw_text,
            vocabulary,
            document_frequency,
            len(requests),
        )
        for request in requests
    }

    grouped: list[list[CitizenRequest]] = []

    for request in requests:

        placed = False

        for group in grouped:

            representative = group[0]

            if not same_cluster_domain(
                request,
                representative,
            ):
                continue

            similarity = cosine_similarity(
                vectors[request.id],
                vectors[representative.id],
            )

            if similarity >= similarity_threshold:
                group.append(request)
                placed = True
                break

        if not placed:
            grouped.append([request])

    clusters: list[SemanticClusterResponse] = []

    for group in grouped:

        if len(group) < 2:
            continue

        representative = max(
            group,
            key=lambda request: len(
                tokenize(request.raw_text)
            ),
        )

        similarities = []

        for request in group:
            if request.id == representative.id:
                continue

            similarities.append(
                cosine_similarity(
                    vectors[representative.id],
                    vectors[request.id],
                )
            )

        average_similarity = (
            sum(similarities) / len(similarities)
            if similarities
            else 1.0
        )

        members = []

        for request in group:

            similarity = cosine_similarity(
                vectors[representative.id],
                vectors[request.id],
            )

            members.append(
                SemanticClusterMember(
                    request_id=request.id,
                    anonymous_reference=request.anonymous_reference,
                    similarity_score=similarity,
                )
            )

        clusters.append(
            SemanticClusterResponse(
                cluster_id=create_cluster_id(
                    [request.id for request in group]
                ),
                category=representative.category,
                representative_issue=representative.raw_text,
                request_count=len(group),
                members=members,
                average_similarity=round(
                    average_similarity,
                    2,
                ),
            )
        )

    return clusters

def get_regional_clusters(
    db: Session,
    region_id: int,
    similarity_threshold: float = 0.60,
):
    requests = db.scalars(
        select(CitizenRequest)
        .where(
            CitizenRequest.region_id == region_id
        )
        .order_by(
            CitizenRequest.created_at.asc()
        )
    ).all()

    return cluster_requests(
        requests=requests,
        similarity_threshold=similarity_threshold,
    )