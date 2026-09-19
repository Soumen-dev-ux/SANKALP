import type { DevelopmentInsight } from "../../types/dashboard";

interface DevelopmentInsightCardsProps {
  insights: DevelopmentInsight[];
}

function getLevelClass(level: string) {
  switch (level) {
    case "High":
      return "bg-red-50 text-red-700 border-red-200";

    case "Moderate":
      return "bg-yellow-50 text-yellow-700 border-yellow-200";

    case "Low":
      return "bg-green-50 text-green-700 border-green-200";

    default:
      return "bg-gray-50 text-gray-700 border-gray-200";
  }
}

function getProgressWidth(value: number) {
  return `${Math.min(Math.max(value, 0), 100)}%`;
}

export default function DevelopmentInsightCards({
  insights,
}: DevelopmentInsightCardsProps) {
  if (insights.length === 0) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center shadow-sm">
        <h3 className="font-semibold text-gray-900">
          No development insights available
        </h3>

        <p className="mt-2 text-sm text-gray-500">
          There is not enough citizen request data to generate
          regional insight cards yet.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      {insights.map((insight) => (
        <article
          key={`${insight.region_id}-${insight.category}`}
          className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm"
        >
          {/* Header */}
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
                Development Signal
              </p>

              <h3 className="mt-1 text-xl font-semibold text-gray-900">
                {insight.category}
              </h3>
            </div>

            <span
              className={`rounded-full border px-3 py-1 text-xs font-semibold ${getLevelClass(
                insight.insight_level
              )}`}
            >
              {insight.insight_level}
            </span>
          </div>

          {/* Main metrics */}
          <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
            <div>
              <p className="text-xs text-gray-500">
                Requests
              </p>

              <p className="mt-1 text-xl font-bold text-gray-900">
                {insight.request_count}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">
                Demand
              </p>

              <p className="mt-1 text-xl font-bold text-gray-900">
                {insight.demand_score.toFixed(1)}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">
                Gap
              </p>

              <p className="mt-1 text-xl font-bold text-gray-900">
                {insight.gap_score.toFixed(1)}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">
                Projects
              </p>

              <p className="mt-1 text-xl font-bold text-gray-900">
                {insight.project_count}
              </p>
            </div>
          </div>

          {/* Coverage */}
          <div className="mt-6">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium text-gray-700">
                Infrastructure Coverage
              </span>

              <span className="font-semibold text-gray-900">
                {insight.infrastructure_coverage.toFixed(1)}%
              </span>
            </div>

            <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-100">
              <div
                className="h-full rounded-full bg-blue-500"
                style={{
                  width: getProgressWidth(
                    insight.infrastructure_coverage
                  ),
                }}
              />
            </div>
          </div>

          {/* Project coverage */}
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm">
              <span className="font-medium text-gray-700">
                Project Coverage
              </span>

              <span className="font-semibold text-gray-900">
                {insight.project_coverage.toFixed(1)}%
              </span>
            </div>

            <div className="mt-2 h-2 overflow-hidden rounded-full bg-gray-100">
              <div
                className="h-full rounded-full bg-green-500"
                style={{
                  width: getProgressWidth(
                    insight.project_coverage
                  ),
                }}
              />
            </div>
          </div>

          {/* Evidence */}
          <div className="mt-6 border-t border-gray-100 pt-5">
            <h4 className="text-sm font-semibold text-gray-900">
              Evidence
            </h4>

            {insight.evidence.length > 0 ? (
              <ul className="mt-3 space-y-2">
                {insight.evidence.map((item, index) => (
                  <li
                    key={index}
                    className="flex gap-2 text-sm text-gray-600"
                  >
                    <span className="mt-1 text-blue-500">
                      •
                    </span>

                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="mt-2 text-sm text-gray-500">
                No evidence details available.
              </p>
            )}
          </div>

          {/* Data warnings */}
          {insight.data_warnings.length > 0 && (
            <div className="mt-5 rounded-lg border border-yellow-200 bg-yellow-50 p-4">
              <h4 className="text-sm font-semibold text-yellow-800">
                Data warnings
              </h4>

              <ul className="mt-2 space-y-1">
                {insight.data_warnings.map((warning, index) => (
                  <li
                    key={index}
                    className="text-xs text-yellow-700"
                  >
                    • {warning}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </article>
      ))}
    </div>
  );
}