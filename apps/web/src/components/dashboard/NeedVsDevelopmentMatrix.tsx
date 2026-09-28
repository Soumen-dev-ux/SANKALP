import React from "react";
import type { NeedVsDevelopment } from "../../types/intelligence";

interface Props {
  data: NeedVsDevelopment | null;
  loading: boolean;
}

export const NeedVsDevelopmentMatrix: React.FC<Props> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse">
        Calculating Need vs. Development signals...
      </div>
    );
  }

  if (!data || data.categories.length === 0) {
    return (
      <div className="p-6 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700/50">
        No need vs. development correlation data available for this region.
      </div>
    );
  }

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="text-amber-400">⚖️</span> Need vs. Development Matrix
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Comparative synthesis of Citizen Demand vs. Infrastructure Coverage vs. Active Government Projects.
          </p>
        </div>
        <span className="px-3 py-1 bg-amber-500/10 text-amber-300 text-xs font-semibold rounded-full border border-amber-500/20">
          Transparent Signals
        </span>
      </div>

      <div className="space-y-4">
        {data.categories.map((cat) => (
          <div
            key={cat.category}
            className={`p-4 rounded-xl border transition-all duration-200 ${
              cat.misalignment_flag
                ? "bg-rose-950/20 border-rose-500/40 shadow-rose-950/30 shadow-lg"
                : "bg-slate-800/40 border-slate-700/50 hover:border-slate-600"
            }`}
          >
            <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-200 text-base">{cat.category}</span>
                {cat.misalignment_flag && (
                  <span className="px-2 py-0.5 bg-rose-500/20 text-rose-300 text-xs font-bold rounded-md border border-rose-500/30 animate-pulse">
                    CRITICAL GAP DETECTED
                  </span>
                )}
              </div>
              <span className="text-xs font-medium text-slate-400 bg-slate-900/60 px-3 py-1 rounded-lg border border-slate-800">
                {cat.status_summary}
              </span>
            </div>

            {/* Metric Bars Comparison */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3 pt-3 border-t border-slate-800/60 text-xs">
              {/* Citizen Demand Volume */}
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400">Citizen Demand Share:</span>
                  <span className="font-bold text-sky-400">{cat.demand_share_percent}% ({cat.demand_volume} requests)</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-sky-500 h-full rounded-full"
                    style={{ width: `${Math.min(cat.demand_share_percent, 100)}%` }}
                  />
                </div>
              </div>

              {/* Infrastructure Coverage */}
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400">Infra Coverage:</span>
                  <span className="font-bold text-emerald-400">
                    {cat.infrastructure_coverage_percent}% (Score: {cat.infrastructure_quality_score})
                  </span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-emerald-500 h-full rounded-full"
                    style={{ width: `${Math.min(cat.infrastructure_coverage_percent, 100)}%` }}
                  />
                </div>
              </div>

              {/* Government Projects Count */}
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400">Government Projects:</span>
                  <span className="font-bold text-purple-400">
                    {cat.project_count} Total ({cat.ongoing_project_count} Ongoing)
                  </span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-purple-500 h-full rounded-full"
                    style={{ width: `${Math.min(cat.project_count * 25, 100)}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
