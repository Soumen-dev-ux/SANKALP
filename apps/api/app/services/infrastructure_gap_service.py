from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.models.infrastructure import Infrastructure
from app.models.region import Region


def get_infrastructure_gap(
    db: Session,
    region_id: int,
):
    region = (
        db.query(Region)
        .filter(Region.id == region_id)
        .first()
    )

    if not region:
        return None

    total_requests = (
        db.query(func.count(CitizenRequest.id))
        .filter(
            CitizenRequest.region_id == region_id
        )
        .scalar()
        or 0
    )

    category_rows = (
        db.query(
            CitizenRequest.category,
            func.count(CitizenRequest.id).label(
                "request_count"
            ),
        )
        .filter(
            CitizenRequest.region_id == region_id
        )
        .group_by(CitizenRequest.category)
        .all()
    )

    categories = []

    for category, request_count in category_rows:

        category_name = (
            category
            if category
            else "Uncategorized"
        )

        if total_requests > 0:
            demand_score = (
                request_count / total_requests
            ) * 100
        else:
            demand_score = 0

        infrastructure_rows = (
            db.query(Infrastructure)
            .filter(
                Infrastructure.region_id == region_id,
                Infrastructure.category
                == category_name,
            )
            .all()
        )

        if infrastructure_rows:
            infrastructure_data_available = True
            coverage_values = [
                item.coverage_percent
                for item in infrastructure_rows
                if item.coverage_percent is not None
            ]

            quality_values = [
                item.quality_score
                for item in infrastructure_rows
                if item.quality_score is not None
            ]

            if coverage_values:
                infrastructure_coverage = (
                    sum(coverage_values)
                    / len(coverage_values)
                )
            else:
                infrastructure_coverage = 0

            if quality_values:
                infrastructure_quality = (
                    sum(quality_values)
                    / len(quality_values)
                )
            else:
                infrastructure_quality = 0

        else:
            infrastructure_data_available = False
            infrastructure_coverage = 0
            infrastructure_quality = 0

        gap_score = (
            demand_score
            * (1 - infrastructure_coverage / 100)
        )

        categories.append(
            {
                "category": category_name,
                "demand_score": round(
                    demand_score,
                    2,
                ),
                "infrastructure_coverage": round(
                    infrastructure_coverage,
                    2,
                ),
                "infrastructure_quality": round(
                    infrastructure_quality,
                    2,
                ),
                "gap_score": round(
                    gap_score,
                    2,
                ),
                "request_count": request_count,
                "infrastructure_data_available": (
                    infrastructure_data_available
                ),
            }
        )

    categories.sort(
        key=lambda item: item["gap_score"],
        reverse=True,
    )

    return {
        "region_id": region.id,
        "region_name": region.name,
        "total_requests": total_requests,
        "categories": categories,
    }