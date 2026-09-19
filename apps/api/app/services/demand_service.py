from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.citizen_request import CitizenRequest
from app.models.region import Region


def get_regional_demand(
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

    if total_requests == 0:
        return {
            "region_id": region.id,
            "region_name": region.name,
            "total_requests": 0,
            "categories": [],
        }

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
        .order_by(
            func.count(CitizenRequest.id).desc()
        )
        .all()
    )

    categories = []

    for category, request_count in category_rows:
        category_name = (
            category
            if category
            else "Uncategorized"
        )

        demand_score = (
            request_count / total_requests
        ) * 100

        categories.append(
            {
                "category": category_name,
                "request_count": request_count,
                "demand_score": round(
                    demand_score,
                    2,
                ),
            }
        )

    return {
        "region_id": region.id,
        "region_name": region.name,
        "total_requests": total_requests,
        "categories": categories,
    }