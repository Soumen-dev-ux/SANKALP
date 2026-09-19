export interface Region {
  id: number;
  name: string;
}

export interface RegionSummary {
  id: number;
  name: string;
  demographics_count: number;
  infrastructure_count: number;
  project_count: number;
  request_count: number;
}

export interface CategoryDemand {
  category: string;
  request_count: number;
  demand_score: number;
}

export interface RegionalDemand {
  region_id: number;
  region_name: string;
  total_requests: number;
  categories: CategoryDemand[];
}

export interface InfrastructureGap {
  category: string;
  demand_score: number;
  infrastructure_coverage: number;
  infrastructure_quality: number;
  gap_score: number;
  request_count: number;
  infrastructure_data_available: boolean;
}

export interface RegionalInfrastructureGap {
  region_id: number;
  region_name: string;
  total_requests: number;
  categories: InfrastructureGap[];
}

export interface DevelopmentInsight {
  region_id: number;
  region_name: string;
  category: string;
  request_count: number;
  demand_score: number;
  infrastructure_coverage: number;
  infrastructure_quality: number;
  gap_score: number;
  project_count: number;
  project_coverage: number;
  population: number | null;
  population_density: number | null;
  insight_level: string;
  evidence: string[];
  data_warnings: string[];
}

export interface RegionalDevelopmentInsight {
  region_id: number;
  region_name: string;
  insights: DevelopmentInsight[];
}

export interface GovernmentProject {
  id: number;
  region_id: number;
  name: string;
  category: string;
  description: string | null;
  status: "Planned" | "Ongoing" | "Completed" | "Cancelled";
  budget: number | null;
  implementing_agency: string | null;
  start_date: string | null;
  expected_completion_date: string | null;
  actual_completion_date: string | null;
  latitude: number | null;
  longitude: number | null;
}

export interface InfrastructureRecord {
  id: number;
  region_id: number;
  category: string;
  infrastructure_type: string;
  name: string | null;
  capacity: number | null;
  coverage_percent: number | null;
  quality_score: number | null;
  operational: boolean;
  latitude: number | null;
  longitude: number | null;
}

export interface CitizenRequestLocation {
  id: number;
  anonymous_reference: string;
  raw_text: string;
  category: string | null;
  status: string;
  latitude: number | null;
  longitude: number | null;
  created_at: string;
}