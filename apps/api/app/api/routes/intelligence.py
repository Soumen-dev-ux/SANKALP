import csv
import io
import json
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.rbac import require_analyst, require_roles
from app.db.session import get_db
from app.models.region import Region
from app.models.user import User
from app.schemas.intelligence import (
    RegionalIntelligenceResponse,
    MultiRegionCompareResponse,
    RegionalTrendsResponse,
    InfrastructureAnalyticsResponse,
    ProjectEffectivenessResponse,
    RegionalHotspotsResponse,
    NeedVsDevelopmentResponse,
    AIExplanationRequest,
    AIExplanationResponse
)
from app.services.intelligence.regional_intelligence_service import RegionalIntelligenceService
from app.services.intelligence.infrastructure_analysis import compute_infrastructure_analytics
from app.services.intelligence.project_analysis import compute_project_effectiveness
from app.services.intelligence.trend_analysis import compute_regional_trends
from app.services.intelligence.hotspot_analysis import compute_regional_hotspots

router = APIRouter(prefix="/intelligence", tags=["Intelligence"])


@router.get("/regions/compare", response_model=MultiRegionCompareResponse)
def compare_regions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    return RegionalIntelligenceService.compare_regions(db)


@router.get("/regions/{region_id}", response_model=RegionalIntelligenceResponse)
def get_regional_intelligence(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    try:
        return RegionalIntelligenceService.get_regional_intelligence(db, region_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/regions/{region_id}/trends", response_model=RegionalTrendsResponse)
def get_regional_trends(
    region_id: int,
    interval: str = Query("monthly", pattern="^(daily|weekly|monthly)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    return compute_regional_trends(db, region_id, region.name, interval=interval)


@router.get("/regions/{region_id}/infrastructure", response_model=InfrastructureAnalyticsResponse)
def get_infrastructure_analytics(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    return compute_infrastructure_analytics(db, region_id, region.name)


@router.get("/regions/{region_id}/projects", response_model=ProjectEffectivenessResponse)
def get_project_effectiveness(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    return compute_project_effectiveness(db, region_id, region.name)


@router.get("/regions/{region_id}/hotspots", response_model=RegionalHotspotsResponse)
def get_regional_hotspots(
    region_id: int,
    grid_size: float = Query(0.05, ge=0.01, le=0.5),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    region = db.query(Region).filter(Region.id == region_id).first()
    if not region:
        raise HTTPException(status_code=404, detail=f"Region {region_id} not found")
    return compute_regional_hotspots(db, region_id, region.name, grid_size_degree=grid_size)


@router.get("/regions/{region_id}/need-vs-development", response_model=NeedVsDevelopmentResponse)
def get_need_vs_development(
    region_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    try:
        return RegionalIntelligenceService.analyze_need_vs_development(db, region_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/explanation", response_model=AIExplanationResponse)
def generate_ai_explanation(
    payload: AIExplanationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst)
):
    try:
        return RegionalIntelligenceService.generate_ai_explanation(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/export")
def export_intelligence_data(
    region_id: int | None = None,
    format: str = Query("json", pattern="^(json|csv)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "reviewer", "analyst"))
):
    regions_to_export = []
    if region_id:
        r = db.query(Region).filter(Region.id == region_id).first()
        if r:
            regions_to_export.append(r)
    else:
        regions_to_export = db.query(Region).all()

    data = [RegionalIntelligenceService.get_regional_intelligence(db, r.id).model_dump() for r in regions_to_export]

    if format == "json":
        content = json.dumps(data, indent=2, default=str)
        return Response(content=content, media_type="application/json", headers={"Content-Disposition": "attachment; filename=sankalp_intelligence.json"})

    # CSV Format
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Region ID", "Region Code", "Region Name", "Total Requests", "Infra Coverage %", "Infra Quality", "Total Projects", "Ongoing Projects"])

    for item in data:
        writer.writerow([
            item["region_id"],
            item["region_code"],
            item["region_name"],
            item["request_metrics"]["total_requests"],
            item["infrastructure_metrics"]["average_coverage"],
            item["infrastructure_metrics"]["average_quality"],
            item["project_metrics"]["total_projects"],
            item["project_metrics"]["ongoing"]
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sankalp_intelligence.csv"}
    )
