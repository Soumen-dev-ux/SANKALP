from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.citizen_request import CitizenRequest
from app.schemas.intelligence import TrendPoint, RegionalTrendsResponse


def compute_regional_trends(
    db: Session,
    region_id: int,
    region_name: str,
    interval: str = "monthly"
) -> RegionalTrendsResponse:
    requests = (
        db.query(CitizenRequest)
        .filter(CitizenRequest.region_id == region_id)
        .order_by(CitizenRequest.created_at.asc())
        .all()
    )
    
    if not requests:
        return RegionalTrendsResponse(
            region_id=region_id,
            region_name=region_name,
            interval=interval,
            trends=[],
            growth_rate_percent=0.0,
            dominant_rising_category=None
        )
    
    grouped: dict[str, list[CitizenRequest]] = {}
    
    for req in requests:
        dt = req.created_at
        if not dt:
            dt = datetime.utcnow()
            
        if interval == "daily":
            key = dt.strftime("%Y-%m-%d")
        elif interval == "weekly":
            # Year-Week format e.g. 2026-W38
            key = dt.strftime("%Y-W%U")
        else:
            # Monthly format e.g. 2026-09
            key = dt.strftime("%Y-%m")
            
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(req)
        
    trend_points: list[TrendPoint] = []
    category_totals: dict[str, int] = {}
    
    sorted_keys = sorted(grouped.keys())
    for key in sorted_keys:
        items = grouped[key]
        cats: dict[str, int] = {}
        for item in items:
            c = item.category or "Uncategorized"
            cats[c] = cats.get(c, 0) + 1
            category_totals[c] = category_totals.get(c, 0) + 1
            
        trend_points.append(
            TrendPoint(
                timestamp=key,
                total_requests=len(items),
                categories=cats
            )
        )
        
    # Calculate growth rate between first half and second half of time series
    growth_rate = 0.0
    if len(trend_points) >= 2:
        mid = len(trend_points) // 2
        first_half_vol = sum(tp.total_requests for tp in trend_points[:mid])
        second_half_vol = sum(tp.total_requests for tp in trend_points[mid:])
        
        if first_half_vol > 0:
            growth_rate = round(((second_half_vol - first_half_vol) / first_half_vol) * 100.0, 1)
            
    dominant_cat = max(category_totals.items(), key=lambda x: x[1])[0] if category_totals else None
    
    return RegionalTrendsResponse(
        region_id=region_id,
        region_name=region_name,
        interval=interval,
        trends=trend_points,
        growth_rate_percent=growth_rate,
        dominant_rising_category=dominant_cat
    )
