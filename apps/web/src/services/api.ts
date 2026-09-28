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

// Interceptor to inject JWT auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("sankalp_token");
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Auth Types & API ---
export interface User {
  id: number;
  email: string;
  full_name: string;
  role: "admin" | "reviewer" | "analyst" | "viewer";
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  role?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const loginUser = async (payload: LoginPayload): Promise<TokenResponse> => {
  const response = await api.post<TokenResponse>("/auth/login", payload);
  return response.data;
};

export const registerUser = async (payload: RegisterPayload): Promise<User> => {
  const response = await api.post<User>("/auth/register", payload);
  return response.data;
};

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get<User>("/auth/me");
  return response.data;
};

// --- Reviewer Queue Types & API ---
export interface PendingReview {
  request_id: number;
  anonymous_reference: string;
  raw_text: string;
  category: string | null;
  issue: string | null;
  location_text: string | null;
  confidence_review_required: boolean;
  review_status: string;
  created_at: string;
}

export interface ReviewActionPayload {
  status: "approved" | "corrected";
  reviewer_note?: string | null;
  reviewed_category?: string | null;
  reviewed_issue?: string | null;
  reviewed_location?: string | null;
}

export interface ReviewAction {
  id: number;
  request_id: number;
  reviewer_id: number;
  status: string;
  reviewer_note: string | null;
  reviewed_category: string | null;
  reviewed_issue: string | null;
  reviewed_location: string | null;
  created_at: string;
}

export const getPendingReviews = async (): Promise<PendingReview[]> => {
  const response = await api.get<PendingReview[]>("/reviews/pending");
  return response.data;
};

export const submitReviewAction = async (
  requestId: number,
  payload: ReviewActionPayload
): Promise<ReviewAction> => {
  const response = await api.post<ReviewAction>(
    `/reviews/requests/${requestId}`,
    payload
  );
  return response.data;
};

export const getReviewHistory = async (
  requestId: number
): Promise<ReviewAction[]> => {
  const response = await api.get<ReviewAction[]>(
    `/reviews/requests/${requestId}/history`
  );
  return response.data;
};

// --- Existing Dashboard & Citizen APIs ---
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

// --- Phase 7 Intelligence APIs ---
import type {
  RegionalIntelligence,
  MultiRegionCompare,
  RegionalTrends,
  InfrastructureAnalytics,
  ProjectEffectiveness,
  RegionalHotspots,
  NeedVsDevelopment,
  AIExplanation,
} from "../types/intelligence";

export const getRegionalIntelligence = async (
  regionId: number
): Promise<RegionalIntelligence> => {
  const response = await api.get<RegionalIntelligence>(
    `/intelligence/regions/${regionId}`
  );
  return response.data;
};

export const getMultiRegionCompare = async (): Promise<MultiRegionCompare> => {
  const response = await api.get<MultiRegionCompare>(
    `/intelligence/regions/compare`
  );
  return response.data;
};

export const getRegionalTrends = async (
  regionId: number,
  interval: "daily" | "weekly" | "monthly" = "monthly"
): Promise<RegionalTrends> => {
  const response = await api.get<RegionalTrends>(
    `/intelligence/regions/${regionId}/trends?interval=${interval}`
  );
  return response.data;
};

export const getInfrastructureAnalytics = async (
  regionId: number
): Promise<InfrastructureAnalytics> => {
  const response = await api.get<InfrastructureAnalytics>(
    `/intelligence/regions/${regionId}/infrastructure`
  );
  return response.data;
};

export const getProjectEffectiveness = async (
  regionId: number
): Promise<ProjectEffectiveness> => {
  const response = await api.get<ProjectEffectiveness>(
    `/intelligence/regions/${regionId}/projects`
  );
  return response.data;
};

export const getRegionalHotspots = async (
  regionId: number,
  gridSize: number = 0.05
): Promise<RegionalHotspots> => {
  const response = await api.get<RegionalHotspots>(
    `/intelligence/regions/${regionId}/hotspots?grid_size=${gridSize}`
  );
  return response.data;
};

export const getNeedVsDevelopment = async (
  regionId: number
): Promise<NeedVsDevelopment> => {
  const response = await api.get<NeedVsDevelopment>(
    `/intelligence/regions/${regionId}/need-vs-development`
  );
  return response.data;
};

export const getAIExplanation = async (
  regionId: number,
  category?: string
): Promise<AIExplanation> => {
  const response = await api.post<AIExplanation>(
    `/intelligence/explanation`,
    { region_id: regionId, category }
  );
  return response.data;
};

export const downloadIntelligenceExport = async (
  regionId?: number,
  format: "json" | "csv" = "json"
): Promise<void> => {
  const url = `/intelligence/export?format=${format}${
    regionId ? `&region_id=${regionId}` : ""
  }`;
  const response = await api.get(url, { responseType: "blob" });
  const blob = new Blob([response.data], {
    type: format === "json" ? "application/json" : "text/csv",
  });
  const downloadUrl = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = downloadUrl;
  link.setAttribute(
    "download",
    `sankalp_intelligence_${regionId || "all"}.${format}`
  );
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export default api;