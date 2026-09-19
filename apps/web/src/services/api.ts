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

export default api;