from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.infrastructure import Infrastructure
from app.schemas.intelligence import (
    InfrastructureMetrics,
    InfrastructureAnalyticsCategory,
    InfrastructureAnalyticsResponse
)


def compute_infrastructure_metrics(db: Session, region_id: int) -> InfrastructureMetrics:
    infra_list = db.query(Infrastructure).filter(Infrastructure.region_id == region_id).all()
    
    total_units = len(infra_list)
    if total_units == 0:
        return InfrastructureMetrics(
            total_units=0,
            operational_units=0,
            non_operational_units=0,
            average_coverage=0.0,
            average_quality=0.0
        )
    
    operational_units = sum(1 for item in infra_list if item.operational)
    non_operational_units = total_units - operational_units
    
    coverages = [item.coverage_percent for item in infra_list if item.coverage_percent is not None]
    qualities = [item.quality_score for item in infra_list if item.quality_score is not None]
    
    avg_coverage = round(sum(coverages) / len(coverages), 1) if coverages else 0.0
    avg_quality = round(sum(qualities) / len(qualities), 2) if qualities else 0.0
    
    return InfrastructureMetrics(
        total_units=total_units,
        operational_units=operational_units,
        non_operational_units=non_operational_units,
        average_coverage=avg_coverage,
        average_quality=avg_quality
    )


def compute_infrastructure_analytics(db: Session, region_id: int, region_name: str) -> InfrastructureAnalyticsResponse:
    infra_list = db.query(Infrastructure).filter(Infrastructure.region_id == region_id).all()
    total_units = len(infra_list)
    
    if total_units == 0:
        return InfrastructureAnalyticsResponse(
            region_id=region_id,
            region_name=region_name,
            total_infrastructure_units=0,
            overall_operational_rate=0.0,
            overall_average_coverage=0.0,
            overall_average_quality=0.0,
            categories=[]
        )
    
    metrics = compute_infrastructure_metrics(db, region_id)
    op_rate = round((metrics.operational_units / total_units) * 100.0, 1)
    
    # Group by category
    category_map: dict[str, list[Infrastructure]] = {}
    for item in infra_list:
        cat = item.category or "General"
        if cat not in category_map:
            category_map[cat] = []
        category_map[cat].append(item)
    
    category_list: list[InfrastructureAnalyticsCategory] = []
    for cat, items in category_map.items():
        cat_total = len(items)
        cat_op = sum(1 for i in items if i.operational)
        cat_covs = [i.coverage_percent for i in items if i.coverage_percent is not None]
        cat_quals = [i.quality_score for i in items if i.quality_score is not None]
        cat_caps = [i.capacity for i in items if i.capacity is not None]
        
        category_list.append(
            InfrastructureAnalyticsCategory(
                category=cat,
                total_units=cat_total,
                operational_units=cat_op,
                average_coverage=round(sum(cat_covs) / len(cat_covs), 1) if cat_covs else 0.0,
                average_quality=round(sum(cat_quals) / len(cat_quals), 2) if cat_quals else 0.0,
                total_capacity=sum(cat_caps)
            )
        )
    
    return InfrastructureAnalyticsResponse(
        region_id=region_id,
        region_name=region_name,
        total_infrastructure_units=total_units,
        overall_operational_rate=op_rate,
        overall_average_coverage=metrics.average_coverage,
        overall_average_quality=metrics.average_quality,
        categories=category_list
    )
