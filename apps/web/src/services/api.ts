import axios from "axios";
import type {
  Region,
  RegionSummary,
  RegionalDemand,
  RegionalInfrastructureGap,
  RegionalDevelopmentInsight,
  GovernmentProject,
  InfrastructureRecord,
  CitizenRequestLocation,
} from "../types/dashboard";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json",
    },
});
export const getRegions = async (): Promise<Region[]> => {
  const response = await api.get<Region[]>("/regions");
  return response.data;
};

export const getRegionSummary = async (
  regionId: number
): Promise<RegionSummary> => {
  const response = await api.get<RegionSummary>(
    `/regions/${regionId}/summary`
  );

  return response.data;
};

export const getRegionalDemand = async (
  regionId: number
): Promise<RegionalDemand> => {
  const response = await api.get<RegionalDemand>(
    `/demand/regions/${regionId}`
  );

  return response.data;
};

export const getInfrastructureGap = async (
  regionId: number
): Promise<RegionalInfrastructureGap> => {
  const response = await api.get<RegionalInfrastructureGap>(
    `/infrastructure-gap/regions/${regionId}`
  );

  return response.data;
};

export const getDevelopmentInsights = async (
  regionId: number
): Promise<RegionalDevelopmentInsight> => {
  const response = await api.get<RegionalDevelopmentInsight>(
    `/development-insights/regions/${regionId}`
  );

  return response.data;
};

export const getRegionProjects = async (
  regionId: number
): Promise<GovernmentProject[]> => {
  const response = await api.get<GovernmentProject[]>(
    `/regions/${regionId}/projects`
  );

  return response.data;
};

export const getRegionInfrastructure = async (
  regionId: number
): Promise<InfrastructureRecord[]> => {
  const response = await api.get<InfrastructureRecord[]>(
    `/regions/${regionId}/infrastructure`
  );

  return response.data;
};

export const getRegionRequests = async (
  regionId: number
): Promise<CitizenRequestLocation[]> => {
  const response = await api.get<CitizenRequestLocation[]>(
    `/regions/${regionId}/requests`
  );

  return response.data;
};

export interface DuplicateCandidate {
  request_id: number;
  anonymous_reference: string;
  category: string | null;
  similarity_score: number;
  match_level: string;
  reason: string;
}

export interface DuplicateCheckResponse {
  is_potential_duplicate: boolean;
  candidates: DuplicateCandidate[];
}

export const checkDuplicateRequests = async (
  payload: {
    raw_text: string;
    category?: string | null;
    region_id?: number | null;
    latitude?: number | null;
    longitude?: number | null;
  }
): Promise<DuplicateCheckResponse> => {
  const response = await api.post<DuplicateCheckResponse>(
    "/requests/duplicate-check",
    {
      ...payload,
      source: "web",
    }
  );

  return response.data;
};

export interface HumanReview {
  request_id: number;
  review_status: "not_required" | "pending" | "approved" | "corrected";
  reviewer_note: string | null;
  reviewed_category: string | null;
  reviewed_issue: string | null;
  reviewed_location: string | null;
  reviewed_at: string | null;
}

export const reviewCitizenRequest = async (
  requestId: number,
  payload: {
    status: "approved" | "corrected";
    reviewer_note?: string | null;
    reviewed_category?: string | null;
    reviewed_issue?: string | null;
    reviewed_location?: string | null;
  }
): Promise<HumanReview> => {
  const response = await api.post<HumanReview>(
    `/requests/${requestId}/review`,
    payload
  );

  return response.data;
};

export default api;