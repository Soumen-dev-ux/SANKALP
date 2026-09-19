import type {
  RegionalInfrastructureGap,
} from "../../types/dashboard";

interface InfrastructureGapSummaryProps {
  infrastructureGap: RegionalInfrastructureGap | null;
}

export default function InfrastructureGapSummary({
  infrastructureGap,
}: InfrastructureGapSummaryProps) {
  if (
    !infrastructureGap ||
    infrastructureGap.categories.length === 0
  ) {
    return null;
  }

  const categories = [...infrastructureGap.categories].sort(
    (a, b) => b.gap_score - a.gap_score
  );

  return (
    <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-5">
      {categories.map((item) => (
        <div
          key={item.category}
          className="rounded-lg border border-gray-200 bg-white p-4"
        >
          <div className="flex items-start justify-between gap-2">
            <p className="truncate text-sm font-medium text-gray-700">
              {item.category}
            </p>

            {!item.infrastructure_data_available && (
              <span className="text-xs text-gray-400">
                No data
              </span>
            )}
          </div>

          <p className="mt-2 text-2xl font-bold text-gray-900">
            {item.gap_score.toFixed(1)}
          </p>

          <p className="mt-1 text-xs text-gray-500">
            Gap score
          </p>

          <div className="mt-3 space-y-1 text-xs text-gray-500">
            <p>
              Demand: {item.demand_score.toFixed(1)}%
            </p>

            <p>
              Coverage:{" "}
              {item.infrastructure_coverage.toFixed(1)}%
            </p>

            <p>
              Quality:{" "}
              {(item.infrastructure_quality * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}