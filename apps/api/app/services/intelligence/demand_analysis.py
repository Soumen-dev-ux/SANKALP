from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.citizen_request import CitizenRequest
from app.schemas.intelligence import RequestMetrics, CategoryDemandMetric


def compute_request_metrics(db: Session, region_id: int) -> RequestMetrics:
    query = db.query(CitizenRequest).filter(CitizenRequest.region_id == region_id)
    total_requests = query.count()
    
    if total_requests == 0:
        return RequestMetrics(
            total_requests=0,
            resolved_requests=0,
            pending_review_requests=0,
            categories=[]
        )
    
    resolved_requests = query.filter(CitizenRequest.status.in_(["resolved", "completed"])).count()
    pending_review = query.filter(CitizenRequest.review_status == "pending").count()
    
    category_counts = (
        db.query(
            func.coalesce(CitizenRequest.category, "Uncategorized").label("cat"),
            func.count(CitizenRequest.id).label("cnt")
        )
        .filter(CitizenRequest.region_id == region_id)
        .group_by("cat")
        .order_by(func.count(CitizenRequest.id).desc())
        .all()
    )
    
    categories = [
        CategoryDemandMetric(
            category=cat,
            count=cnt,
            percentage=round((cnt / total_requests) * 100.0, 1)
        )
        for cat, cnt in category_counts
    ]
    
    return RequestMetrics(
        total_requests=total_requests,
        resolved_requests=resolved_requests,
        pending_review_requests=pending_review,
        categories=categories
    )
