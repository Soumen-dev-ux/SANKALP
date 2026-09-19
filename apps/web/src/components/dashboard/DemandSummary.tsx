import type { RegionalDemand } from "../../types/dashboard";

interface DemandSummaryProps {
  demand: RegionalDemand | null;
}

export default function DemandSummary({
  demand,
}: DemandSummaryProps) {
  if (!demand || demand.categories.length === 0) {
    return null;
  }

  const categories = [...demand.categories].sort(
    (a, b) => b.demand_score - a.demand_score
  );

  return (
    <div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-5">
      {categories.map((item) => (
        <div
          key={item.category}
          className="rounded-lg border border-gray-200 bg-white p-4"
        >
          <p className="truncate text-sm font-medium text-gray-700">
            {item.category}
          </p>

          <p className="mt-2 text-2xl font-bold text-gray-900">
            {item.demand_score.toFixed(1)}%
          </p>

          <p className="mt-1 text-xs text-gray-500">
            {item.request_count} citizen requests
          </p>
        </div>
      ))}
    </div>
  );
}