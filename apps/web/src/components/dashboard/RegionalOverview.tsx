import type {
  RegionalDemand,
  RegionalInfrastructureGap,
  RegionalDevelopmentInsight,
} from "../../types/dashboard";

interface RegionalOverviewProps {
  demand: RegionalDemand | null;
  infrastructureGap: RegionalInfrastructureGap | null;
  insights: RegionalDevelopmentInsight | null;
}

export default function RegionalOverview({
  demand,
  infrastructureGap,
  insights,
}: RegionalOverviewProps) {
  const topDemand = demand?.categories?.length
    ? [...demand.categories].sort(
        (a, b) => b.demand_score - a.demand_score
      )[0]
    : null;

  const topGap = infrastructureGap?.categories?.length
    ? [...infrastructureGap.categories].sort(
        (a, b) => b.gap_score - a.gap_score
      )[0]
    : null;

  const highInsights =
    insights?.insights?.filter(
      (item) => item.insight_level === "High"
    ).length ?? 0;

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <p className="text-sm text-gray-500">
          Highest Citizen Demand
        </p>

        <h3 className="mt-2 text-lg font-semibold text-gray-900">
          {topDemand?.category ?? "No data"}
        </h3>

        {topDemand && (
          <p className="mt-1 text-sm text-gray-500">
            {topDemand.request_count} requests ·{" "}
            {topDemand.demand_score.toFixed(1)}% demand share
          </p>
        )}
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <p className="text-sm text-gray-500">
          Highest Infrastructure Gap
        </p>

        <h3 className="mt-2 text-lg font-semibold text-gray-900">
          {topGap?.category ?? "No data"}
        </h3>

        {topGap && (
          <p className="mt-1 text-sm text-gray-500">
            Gap score: {topGap.gap_score.toFixed(1)}
          </p>
        )}
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
        <p className="text-sm text-gray-500">
          High-Priority Development Signals
        </p>

        <h3 className="mt-2 text-lg font-semibold text-gray-900">
          {highInsights}
        </h3>

        <p className="mt-1 text-sm text-gray-500">
          Based on the current development insight model
        </p>
      </div>
    </div>
  );
}