export interface CategoryDemandMetric {
  category: string;
  count: number;
  percentage: number;
}

export interface RequestMetrics {
  total_requests: number;
  resolved_requests: number;
  pending_review_requests: number;
  categories: CategoryDemandMetric[];
}

export interface InfrastructureMetrics {
  total_units: number;
  operational_units: number;
  non_operational_units: number;
  average_coverage: number;
  average_quality: number;
}

export interface ProjectMetrics {
  total_projects: number;
  planned: number;
  ongoing: number;
  completed: number;
  cancelled: number;
  total_budget: number;
}

export interface DevelopmentSignal {
  category: string;
  demand_score: number;
  infrastructure_coverage: number;
  infrastructure_quality: number;
  gap_score: number;
  project_count: number;
  data_warnings: string[];
}

export interface DataQualitySummary {
  warnings: string[];
  completeness_score: number;
}

export interface RegionalIntelligence {
  region_id: number;
  region_name: string;
  region_code: string;
  request_metrics: RequestMetrics;
  infrastructure_metrics: InfrastructureMetrics;
  project_metrics: ProjectMetrics;
  development_signals: DevelopmentSignal[];
  data_quality: DataQualitySummary;
}

export interface RegionCompareMetrics {
  region_id: number;
  region_name: string;
  region_code: string;
  total_requests: number;
  infrastructure_coverage: number;
  infrastructure_quality: number;
  total_projects: number;
  ongoing_projects: number;
  top_demand_category: string | null;
}

export interface MultiRegionCompare {
  regions: RegionCompareMetrics[];
}

export interface TrendPoint {
  timestamp: string;
  total_requests: number;
  categories: Record<string, number>;
}

export interface RegionalTrends {
  region_id: number;
  region_name: string;
  interval: string;
  trends: TrendPoint[];
  growth_rate_percent: number;
  dominant_rising_category: string | null;
}

export interface InfrastructureAnalyticsCategory {
  category: string;
  total_units: number;
  operational_units: number;
  average_coverage: number;
  average_quality: number;
  total_capacity: number;
}

export interface InfrastructureAnalytics {
  region_id: number;
  region_name: string;
  total_infrastructure_units: number;
  overall_operational_rate: number;
  overall_average_coverage: number;
  overall_average_quality: number;
  categories: InfrastructureAnalyticsCategory[];
}

export interface ProjectEffectivenessCategory {
  category: string;
  total_projects: number;
  planned: number;
  ongoing: number;
  completed: number;
  cancelled: number;
  total_budget: number;
}

export interface ProjectEffectiveness {
  region_id: number;
  region_name: string;
  total_projects: number;
  status_breakdown: Record<string, number>;
  category_alignment: ProjectEffectivenessCategory[];
}

export interface GeographicHotspot {
  hotspot_id: string;
  approx_latitude: number;
  approx_longitude: number;
  radius_km: number;
  request_count: number;
  dominant_category: string;
  categories: Record<string, number>;
}

export interface RegionalHotspots {
  region_id: number;
  region_name: string;
  total_hotspots: number;
  hotspots: GeographicHotspot[];
}

export interface NeedVsDevelopmentCategory {
  category: string;
  demand_volume: number;
  demand_share_percent: number;
  infrastructure_coverage_percent: number;
  infrastructure_quality_score: number;
  project_count: number;
  ongoing_project_count: number;
  misalignment_flag: boolean;
  status_summary: string;
}

export interface NeedVsDevelopment {
  region_id: number;
  region_name: string;
  categories: NeedVsDevelopmentCategory[];
}

export interface AIExplanation {
  region_id: number;
  region_name: string;
  summary: string;
  key_evidence: string[];
  observed_trends: string[];
  data_limitations: string[];
  questions_for_human_review: string[];
}
