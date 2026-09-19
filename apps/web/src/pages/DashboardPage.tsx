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

import {
  getRegions,
  getRegionSummary,
  getRegionalDemand,
  getInfrastructureGap,
  getDevelopmentInsights,
  getRegionProjects,
  getRegionRequests,
  getRegionInfrastructure,
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
        ] = await Promise.all([
          getRegionSummary(selectedRegionId),
          getRegionalDemand(selectedRegionId),
          getInfrastructureGap(selectedRegionId),
          getDevelopmentInsights(selectedRegionId),
          getRegionProjects(selectedRegionId),
          getRegionInfrastructure(selectedRegionId),
          getRegionRequests(selectedRegionId),
        ]);

        setSummary(summaryData);
        setDemand(demandData);
        setInfrastructureGap(infrastructureGapData);
        setInsights(insightsData);
        setProjects(projectsData);
        setInfrastructure(infrastructureData);
        setRequests(requestsData);
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
      : regions.find((r) => r.id === selectedRegionId)?.name;

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
            title="All Regions Overview"
            description="A cross-region view of available citizen, infrastructure, project, and demographic records."
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