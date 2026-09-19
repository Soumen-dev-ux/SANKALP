import type {
  DevelopmentInsight,
  RegionalDemand,
} from "../../types/dashboard";

interface CitizenInsightFlowProps {
  demand: RegionalDemand | null;
  insights: DevelopmentInsight[];
}

function getLevelClasses(level: string) {
  switch (level) {
    case "High":
      return "border-rose-200 bg-rose-50 text-rose-700 shadow-xs shadow-rose-100";

    case "Moderate":
      return "border-amber-200 bg-amber-50 text-amber-700 shadow-xs shadow-amber-100";

    default:
      return "border-emerald-200 bg-emerald-50 text-emerald-700 shadow-xs shadow-emerald-100";
  }
}

function Metric({
  label,
  value,
  suffix = "",
}: {
  label: string;
  value: string | number;
  suffix?: string;
}) {
  return (
    <div className="rounded-xl border border-slate-200/80 bg-slate-50/70 p-3.5 transition-colors hover:bg-slate-100/60">
      <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-lg font-extrabold text-slate-900 tracking-tight">
        {value}
        {suffix}
      </p>
    </div>
  );
}

export default function CitizenInsightFlow({
  demand,
  insights,
}: CitizenInsightFlowProps) {
  if (!demand) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <h3 className="font-semibold text-slate-900">
          Citizen Request → Development Insight
        </h3>
        <p className="mt-2 text-sm text-slate-500">
          Regional demand data is currently unavailable.
        </p>
      </div>
    );
  }

  if (demand.total_requests === 0) {
    return (
      <div className="rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs">
        <h3 className="font-semibold text-slate-900">
          Citizen Request → Development Insight
        </h3>
        <p className="mt-2 text-sm leading-6 text-slate-500">
          No citizen requests are currently recorded for this region. This should be interpreted as an absence of available request data, not as evidence that development needs are absent.
        </p>
      </div>
    );
  }

  const totalRequests = demand.total_requests;

  return (
    <div className="space-y-6">
      {/* Flow header banner */}
      <div className="rounded-2xl border border-blue-200/80 bg-gradient-to-r from-blue-50 via-indigo-50/50 to-white p-5 sm:p-6 shadow-xs">
        <div className="flex items-center gap-2">
          <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-600 text-white font-bold text-xs shadow-sm shadow-blue-500/20">
            ⚡
          </span>
          <h3 className="text-base font-bold text-blue-950">
            Citizen Request → Development Intelligence Pipeline
          </h3>
        </div>

        <p className="mt-2 text-sm leading-relaxed text-blue-900/80">
          Citizen-reported needs are algorithmically mapped into structured analytical signals by combining request volume, existing infrastructure coverage, active government projects, and regional demographic context.
        </p>
      </div>

      {/* Top Level Summary Metrics */}
      <div className="grid gap-3.5 sm:grid-cols-2 md:grid-cols-4">
        <Metric label="Total Requests" value={totalRequests} />
        <Metric label="Categories Detected" value={insights.length} />
        <Metric label="Regional Scope" value={demand.region_name} />
        <Metric label="Analytical Signals" value={insights.length} />
      </div>

      {/* Insight Pipeline Cards */}
      <div className="space-y-5">
        {insights.map((insight) => (
          <div
            key={`${insight.region_id}-${insight.category}`}
            className="group rounded-2xl border border-slate-200/80 bg-white p-6 shadow-xs hover:shadow-md transition-all duration-300"
          >
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between border-b border-slate-100 pb-4">
              <div>
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                  Category Signal
                </span>
                <h4 className="mt-0.5 text-lg font-bold text-slate-900 tracking-tight">
                  {insight.category}
                </h4>
              </div>

              <span
                className={`w-fit rounded-full border px-3.5 py-1 text-xs font-bold ${getLevelClasses(
                  insight.insight_level
                )}`}
              >
                {insight.insight_level} Signal Priority
              </span>
            </div>

            {/* Metrics Grid */}
            <div className="mt-5 grid gap-3 grid-cols-2 sm:grid-cols-3 md:grid-cols-5">
              <Metric label="Requests" value={insight.request_count} />
              <Metric label="Demand Share" value={insight.demand_score} suffix="%" />
              <Metric label="Coverage" value={insight.infrastructure_coverage} suffix="%" />
              <Metric label="Gap Score" value={insight.gap_score} />
              <Metric label="Projects" value={insight.project_count} />
            </div>

            {/* Visual Process Flow */}
            <div className="mt-5 overflow-x-auto pb-2">
              <div className="flex min-w-[720px] items-center gap-2 text-xs font-semibold">
                <div className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2 text-slate-700 shadow-2xs">
                  Citizen Request
                </div>

                <span className="text-slate-300 font-bold">→</span>

                <div className="rounded-xl border border-blue-200 bg-blue-50/80 px-3.5 py-2 text-blue-800 shadow-2xs">
                  {insight.request_count} request{insight.request_count === 1 ? "" : "s"}
                </div>

                <span className="text-slate-300 font-bold">→</span>

                <div className="rounded-xl border border-indigo-200 bg-indigo-50/80 px-3.5 py-2 text-indigo-800 shadow-2xs">
                  {insight.demand_score}% demand
                </div>

                <span className="text-slate-300 font-bold">→</span>

                <div className="rounded-xl border border-amber-200 bg-amber-50/80 px-3.5 py-2 text-amber-800 shadow-2xs">
                  {insight.infrastructure_coverage}% coverage
                </div>

                <span className="text-slate-300 font-bold">→</span>

                <div className="rounded-xl border border-rose-200 bg-rose-50/80 px-3.5 py-2 text-rose-800 shadow-2xs">
                  {insight.gap_score} gap
                </div>

                <span className="text-slate-300 font-bold">→</span>

                <div className="rounded-xl border border-purple-200 bg-purple-50/80 px-3.5 py-2 text-purple-800 shadow-2xs">
                  {insight.project_count} project{insight.project_count === 1 ? "" : "s"}
                </div>
              </div>
            </div>

            {/* Evidence & Details */}
            {insight.evidence.length > 0 && (
              <div className="mt-5 rounded-xl border border-slate-100 bg-slate-50/50 p-4">
                <h5 className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Supporting Evidence
                </h5>
                <ul className="mt-2 space-y-1.5">
                  {insight.evidence.map((item, index) => (
                    <li
                      key={index}
                      className="flex items-start gap-2 text-xs leading-relaxed text-slate-600"
                    >
                      <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-blue-500" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Data Warnings */}
            {insight.data_warnings.length > 0 && (
              <div className="mt-4 rounded-xl border border-amber-200/80 bg-amber-50/70 p-4">
                <p className="text-xs font-bold uppercase tracking-wider text-amber-800">
                  Data Context Warnings
                </p>
                <ul className="mt-1.5 space-y-1">
                  {insight.data_warnings.map((warning, index) => (
                    <li
                      key={index}
                      className="flex items-start gap-2 text-xs leading-relaxed text-amber-900"
                    >
                      <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-500" />
                      <span>{warning}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="rounded-xl border border-slate-200/80 bg-slate-100/60 p-4">
        <p className="text-xs leading-relaxed text-slate-500">
          These signals represent automated analytical insights calculated from current repository datasets. They are meant to inform urban planning and prioritize resource allocation, not replace manual ground verification.
        </p>
      </div>
    </div>
  );
}