import { useEffect, useState } from "react";

import DashboardHeader from "../components/dashboard/DashboardHeader";
import RegionSelector from "../components/dashboard/RegionSelector";
import RegionalSummaryCards from "../components/dashboard/RegionalSummaryCards";
import DashboardSection from "../components/dashboard/DashboardSection";
import RegionalOverview from "../components/dashboard/RegionalOverview";
import DemandChart from "../components/dashboard/DemandChart";
import DemandSummary from "../components/dashboard/DemandSummary";
import InfrastructureGapChart from "../components/dashboard/InfrastructureGapChart";
import InfrastructureGapSummary from "../components/dashboard/InfrastructureGapSummary";
import GovernmentProjectView from "../components/dashboard/GovernmentProjectView";
import DevelopmentInsightCards from "../components/dashboard/DevelopmentInsightCards";
import DashboardDisclaimer from "../components/dashboard/DashboardDisclaimer";
import RegionalComparison from "../components/dashboard/RegionalComparison";
import IntelligenceMap from "../components/dashboard/IntelligenceMap";
import CitizenInsightFlow from "../components/dashboard/CitizenInsightFlow";

// Phase 7 Intelligence Components
import { NeedVsDevelopmentMatrix } from "../components/dashboard/NeedVsDevelopmentMatrix";
import { IntelligenceTrendsChart } from "../components/dashboard/IntelligenceTrendsChart";
import { InfrastructureAnalyticsView } from "../components/dashboard/InfrastructureAnalyticsView";
import { ProjectEffectivenessView } from "../components/dashboard/ProjectEffectivenessView";
import { HotspotMapView } from "../components/dashboard/HotspotMapView";
import { AIIntelligenceSummaryCard } from "../components/dashboard/AIIntelligenceSummaryCard";
import { ExportReportModal } from "../components/dashboard/ExportReportModal";

import {
  getRegions,
  getRegionSummary,
  getRegionalDemand,
  getInfrastructureGap,
  getDevelopmentInsights,
  getRegionProjects,
  getRegionRequests,
  getRegionInfrastructure,
  getRegionalIntelligence,
  getNeedVsDevelopment,
  getRegionalTrends,
  getInfrastructureAnalytics,
  getProjectEffectiveness,
  getRegionalHotspots,
  getAIExplanation,
} from "../services/api";

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

import type {
  RegionalIntelligence,
  NeedVsDevelopment,
  RegionalTrends,
  InfrastructureAnalytics,
  ProjectEffectiveness,
  RegionalHotspots,
  AIExplanation,
} from "../types/intelligence";

export default function DashboardPage() {
  const [regions, setRegions] = useState<Region[]>([]);
  const [selectedRegionId, setSelectedRegionId] = useState<
    number | "all" | null
  >(null);

  const [summary, setSummary] = useState<RegionSummary | null>(null);
  const [demand, setDemand] = useState<RegionalDemand | null>(null);
  const [infrastructureGap, setInfrastructureGap] =
    useState<RegionalInfrastructureGap | null>(null);
  const [insights, setInsights] =
    useState<RegionalDevelopmentInsight | null>(null);
  const [projects, setProjects] = useState<GovernmentProject[]>([]);
  const [regionalSummaries, setRegionalSummaries] = useState<RegionSummary[]>([]);

  const [loading, setLoading] = useState(true);
  const [regionLoading, setRegionLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [infrastructure, setInfrastructure] = useState<InfrastructureRecord[]>([]);
  const [requests, setRequests] = useState<CitizenRequestLocation[]>([]);

  // Phase 7 State
  const [needVsDev, setNeedVsDev] = useState<NeedVsDevelopment | null>(null);
  const [trends, setTrends] = useState<RegionalTrends | null>(null);
  const [trendInterval, setTrendInterval] = useState<"daily" | "weekly" | "monthly">("monthly");
  const [infraAnalytics, setInfraAnalytics] = useState<InfrastructureAnalytics | null>(null);
  const [projectEffectiveness, setProjectEffectiveness] = useState<ProjectEffectiveness | null>(null);
  const [hotspots, setHotspots] = useState<RegionalHotspots | null>(null);
  const [aiExplanation, setAiExplanation] = useState<AIExplanation | null>(null);
  const [aiLoading, setAiLoading] = useState(false);

  /*
   * Load available regions once.
   */
  useEffect(() => {
    const loadRegions = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await getRegions();

        setRegions(data);

        if (data.length > 0) {
          setSelectedRegionId("all");
        }
      } catch (err) {
        console.error(err);
        setError("Unable to load regions.");
      } finally {
        setLoading(false);
      }
    };

    loadRegions();
  }, []);

  const loadAllRegionSummaries = async () => {
    if (regions.length === 0) {
      return;
    }

    try {
      setRegionLoading(true);
      setError(null);

      const summaries = await Promise.all(
        regions.map((region) => getRegionSummary(region.id))
      );

      setRegionalSummaries(summaries);
    } catch (err) {
      console.error(err);
      setError("Unable to load regional summaries.");
    } finally {
      setRegionLoading(false);
    }
  };

  const fetchTrends = async (regionId: number, interval: "daily" | "weekly" | "monthly") => {
    try {
      const data = await getRegionalTrends(regionId, interval);
      setTrends(data);
    } catch (err) {
      console.error("Trends load failed:", err);
    }
  };

  const fetchAIExplanation = async (regionId: number) => {
    try {
      setAiLoading(true);
      const data = await getAIExplanation(regionId);
      setAiExplanation(data);
    } catch (err) {
      console.error("AI Explanation load failed:", err);
    } finally {
      setAiLoading(false);
    }
  };

  /*
   * Load all regional intelligence whenever
   * the selected region changes.
   */
  useEffect(() => {
    if (selectedRegionId === null) {
      return;
    }

    if (selectedRegionId === "all") {
      setSummary(null);
      setDemand(null);
      setInfrastructureGap(null);
      setInsights(null);
      setProjects([]);
      setInfrastructure([]);
      setRequests([]);
      setNeedVsDev(null);
      setTrends(null);
      setInfraAnalytics(null);
      setProjectEffectiveness(null);
      setHotspots(null);
      setAiExplanation(null);

      loadAllRegionSummaries();
      return;
    }

    const loadRegionData = async () => {
      try {
        setRegionLoading(true);
        setError(null);

        const [
          summaryData,
          demandData,
          infrastructureGapData,
          insightsData,
          projectsData,
          infrastructureData,
          requestsData,
          needVsDevData,
          trendsData,
          infraAnalyticsData,
          projEffectivenessData,
          hotspotsData,
        ] = await Promise.all([
          getRegionSummary(selectedRegionId),
          getRegionalDemand(selectedRegionId),
          getInfrastructureGap(selectedRegionId),
          getDevelopmentInsights(selectedRegionId),
          getRegionProjects(selectedRegionId),
          getRegionInfrastructure(selectedRegionId),
          getRegionRequests(selectedRegionId),
          getNeedVsDevelopment(selectedRegionId).catch(() => null),
          getRegionalTrends(selectedRegionId, trendInterval).catch(() => null),
          getInfrastructureAnalytics(selectedRegionId).catch(() => null),
          getProjectEffectiveness(selectedRegionId).catch(() => null),
          getRegionalHotspots(selectedRegionId).catch(() => null),
        ]);

        setSummary(summaryData);
        setDemand(demandData);
        setInfrastructureGap(infrastructureGapData);
        setInsights(insightsData);
        setProjects(projectsData);
        setInfrastructure(infrastructureData);
        setRequests(requestsData);
        setNeedVsDev(needVsDevData);
        setTrends(trendsData);
        setInfraAnalytics(infraAnalyticsData);
        setProjectEffectiveness(projEffectivenessData);
        setHotspots(hotspotsData);

        // Fetch AI narrative asynchronously
        fetchAIExplanation(selectedRegionId);
      } catch (err) {
        console.error(err);
        setError("Unable to load regional intelligence data.");
      } finally {
        setRegionLoading(false);
      }
    };

    loadRegionData();
  }, [selectedRegionId, regions]);

  const selectedRegionName =
    selectedRegionId === "all"
      ? "All Regions"
      : regions.find((r) => r.id === selectedRegionId)?.name || "Region";

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-500">Loading SANKALP dashboard...</p>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <DashboardHeader regionName={selectedRegionName} />

        <RegionSelector
          regions={regions}
          selectedRegionId={selectedRegionId}
          onChange={setSelectedRegionId}
          disabled={regionLoading}
        />

        {error && (
          <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            {error}
          </div>
        )}

        {selectedRegionId === "all" && (
          <DashboardSection
            title="All Regions Intelligence Overview"
            description="A cross-region comparative matrix synthesizing demand signals, infrastructure coverage, and project allocations."
          >
            {regionLoading ? (
              <div className="rounded-xl border border-slate-200 bg-white p-8 text-center">
                <p className="text-sm text-slate-500">
                  Loading regional data...
                </p>
              </div>
            ) : (
              <RegionalComparison summaries={regionalSummaries} />
            )}
          </DashboardSection>
        )}

        {selectedRegionId !== "all" && (
          regionLoading ? (
            <div className="rounded-xl border border-gray-200 bg-white p-8 text-center">
              <p className="text-gray-500">Loading regional intelligence...</p>
            </div>
          ) : (
            <>
              {/* Phase 7 Export & Reporting Bar */}
              <div className="mb-6">
                <ExportReportModal
                  regionId={typeof selectedRegionId === "number" ? selectedRegionId : null}
                  regionName={selectedRegionName}
                />
              </div>

              {/* Phase 7 AI Intelligence Narrative */}
              <div className="mb-6">
                <AIIntelligenceSummaryCard
                  data={aiExplanation}
                  loading={aiLoading}
                  onRequestRefresh={() => {
                    if (typeof selectedRegionId === "number") {
                      fetchAIExplanation(selectedRegionId);
                    }
                  }}
                />
              </div>

              {/* Phase 7 Need vs Development Matrix */}
              <div className="mb-6">
                <NeedVsDevelopmentMatrix
                  data={needVsDev}
                  loading={regionLoading}
                />
              </div>

              {/* Phase 7 Time Series & Citizen Demand Trends */}
              <div className="mb-6">
                <IntelligenceTrendsChart
                  data={trends}
                  loading={regionLoading}
                  onIntervalChange={(newIntv) => {
                    setTrendInterval(newIntv);
                    if (typeof selectedRegionId === "number") {
                      fetchTrends(selectedRegionId, newIntv);
                    }
                  }}
                />
              </div>

              {/* Phase 7 Infrastructure Analytics & Project Effectiveness */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <InfrastructureAnalyticsView
                  data={infraAnalytics}
                  loading={regionLoading}
                />
                <ProjectEffectivenessView
                  data={projectEffectiveness}
                  loading={regionLoading}
                />
              </div>

              {/* Phase 7 Geographic Hotspots */}
              <div className="mb-6">
                <HotspotMapView
                  data={hotspots}
                  loading={regionLoading}
                />
              </div>

              {/* Existing Baseline Visualizations */}
              <RegionalSummaryCards summary={summary} />

              <DashboardSection
                title="Citizen Demand Analysis"
                description="Understand what development needs citizens are reporting most frequently."
              >
                <DemandChart demand={demand} />
                <DemandSummary demand={demand} />
              </DashboardSection>

              <DashboardSection
                title="Infrastructure Gap Analysis"
                description="Compare reported citizen demand with the available infrastructure coverage in the selected region."
              >
                <InfrastructureGapChart infrastructureGap={infrastructureGap} />
                <InfrastructureGapSummary infrastructureGap={infrastructureGap} />
              </DashboardSection>

              <DashboardSection
                title="Geospatial Intelligence"
                description="View available infrastructure, government projects, and geographically tagged citizen requests for the selected region."
              >
                <IntelligenceMap
                  infrastructure={infrastructure}
                  projects={projects}
                  requests={requests}
                />
              </DashboardSection>

              <DashboardSection
                title="Government Projects"
                description="Projects currently recorded for the selected region."
              >
                <GovernmentProjectView projects={projects} />
              </DashboardSection>

              <DashboardSection
                title="Development Insights"
                description="Explainable analytical signals generated from citizen demand, infrastructure conditions, and project context."
              >
                <DevelopmentInsightCards insights={insights?.insights ?? []} />
              </DashboardSection>

              <DashboardSection
                title="Citizen Voice to Development Intelligence"
                description="Trace how citizen-reported needs become structured regional analytical signals."
              >
                <CitizenInsightFlow
                  demand={demand}
                  insights={insights?.insights ?? []}
                />
              </DashboardSection>

              <DashboardSection
                title="Regional Intelligence Overview"
                description="A high-level view of citizen demand, infrastructure gaps, and development signals."
              >
                <RegionalOverview
                  demand={demand}
                  infrastructureGap={infrastructureGap}
                  insights={insights}
                />
              </DashboardSection>

              <DashboardDisclaimer />
            </>
          )
        )}
      </div>
    </main>
  );
}