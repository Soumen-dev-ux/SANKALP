from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class CategoryDemandMetric(BaseModel):
    category: str
    count: int
    percentage: float


class RequestMetrics(BaseModel):
    total_requests: int
    resolved_requests: int = 0
    pending_review_requests: int = 0
    categories: list[CategoryDemandMetric] = []


class InfrastructureMetrics(BaseModel):
    total_units: int
    operational_units: int
    non_operational_units: int
    average_coverage: float
    average_quality: float


class ProjectMetrics(BaseModel):
    total_projects: int
    planned: int
    ongoing: int
    completed: int
    cancelled: int
    total_budget: float = 0.0


class DevelopmentSignal(BaseModel):
    category: str
    demand_score: float
    infrastructure_coverage: float
    infrastructure_quality: float
    gap_score: float
    project_count: int
    data_warnings: list[str] = []


class DataQualitySummary(BaseModel):
    warnings: list[str] = []
    completeness_score: float = 1.0


class RegionalIntelligenceResponse(BaseModel):
    region_id: int
    region_name: str
    region_code: str
    request_metrics: RequestMetrics
    infrastructure_metrics: InfrastructureMetrics
    project_metrics: ProjectMetrics
    development_signals: list[DevelopmentSignal] = []
    data_quality: DataQualitySummary


class RegionCompareMetrics(BaseModel):
    region_id: int
    region_name: str
    region_code: str
    total_requests: int
    infrastructure_coverage: float
    infrastructure_quality: float
    total_projects: int
    ongoing_projects: int
    top_demand_category: str | None = None


class MultiRegionCompareResponse(BaseModel):
    regions: list[RegionCompareMetrics]


class TrendPoint(BaseModel):
    timestamp: str
    total_requests: int
    categories: dict[str, int] = {}


class RegionalTrendsResponse(BaseModel):
    region_id: int
    region_name: str
    interval: str
    trends: list[TrendPoint]
    growth_rate_percent: float = 0.0
    dominant_rising_category: str | None = None


class InfrastructureAnalyticsCategory(BaseModel):
    category: str
    total_units: int
    operational_units: int
    average_coverage: float
    average_quality: float
    total_capacity: int = 0


class InfrastructureAnalyticsResponse(BaseModel):
    region_id: int
    region_name: str
    total_infrastructure_units: int
    overall_operational_rate: float
    overall_average_coverage: float
    overall_average_quality: float
    categories: list[InfrastructureAnalyticsCategory]


class ProjectEffectivenessCategory(BaseModel):
    category: str
    total_projects: int
    planned: int
    ongoing: int
    completed: int
    cancelled: int
    total_budget: float


class ProjectEffectivenessResponse(BaseModel):
    region_id: int
    region_name: str
    total_projects: int
    status_breakdown: dict[str, int]
    category_alignment: list[ProjectEffectivenessCategory]


class GeographicHotspot(BaseModel):
    hotspot_id: str
    approx_latitude: float
    approx_longitude: float
    radius_km: float
    request_count: int
    dominant_category: str
    categories: dict[str, int]


class RegionalHotspotsResponse(BaseModel):
    region_id: int
    region_name: str
    total_hotspots: int
    hotspots: list[GeographicHotspot]


class NeedVsDevelopmentCategory(BaseModel):
    category: str
    demand_volume: int
    demand_share_percent: float
    infrastructure_coverage_percent: float
    infrastructure_quality_score: float
    project_count: int
    ongoing_project_count: int
    misalignment_flag: bool
    status_summary: str


class NeedVsDevelopmentResponse(BaseModel):
    region_id: int
    region_name: str
    categories: list[NeedVsDevelopmentCategory]


class AIExplanationRequest(BaseModel):
    region_id: int
    category: str | None = None


class AIExplanationResponse(BaseModel):
    region_id: int
    region_name: str
    summary: str
    key_evidence: list[str]
    observed_trends: list[str]
    data_limitations: list[str]
    questions_for_human_review: list[str]


class ExportIntelligenceRequest(BaseModel):
    region_id: int | None = None
    format: str = Field("json", pattern="^(json|csv)$")
