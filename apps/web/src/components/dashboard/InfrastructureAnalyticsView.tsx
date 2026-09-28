import React from "react";
import type { InfrastructureAnalytics } from "../../types/intelligence";

interface Props {
  data: InfrastructureAnalytics | null;
  loading: boolean;
}

export const InfrastructureAnalyticsView: React.FC<Props> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse bg-slate-900/60 rounded-2xl border border-slate-800">
        Analyzing physical infrastructure performance...
      </div>
    );
  }

  if (!data || data.categories.length === 0) {
    return (
      <div className="p-6 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700/50">
        No infrastructure records registered for this region.
      </div>
    );
  }

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="text-emerald-400">🏗️</span> Infrastructure Asset Analytics
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Operational status, capacity, coverage, and quality distribution by sector.
          </p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-300 text-xs font-semibold rounded-full border border-emerald-500/20">
          {data.total_infrastructure_units} Units Registered
        </span>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
          <span className="text-xs text-slate-400 font-medium block">Operational Rate</span>
          <span className="text-2xl font-extrabold text-emerald-400 mt-1 block">
            {data.overall_operational_rate}%
          </span>
        </div>

        <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
          <span className="text-xs text-slate-400 font-medium block">Average Coverage</span>
          <span className="text-2xl font-extrabold text-sky-400 mt-1 block">
            {data.overall_average_coverage}%
          </span>
        </div>

        <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
          <span className="text-xs text-slate-400 font-medium block">Asset Quality Index</span>
          <span className="text-2xl font-extrabold text-indigo-400 mt-1 block">
            {data.overall_average_quality} <span className="text-xs font-normal text-slate-400">/ 1.0</span>
          </span>
        </div>
      </div>

      {/* Category List */}
      <div className="space-y-3">
        {data.categories.map((cat) => {
          const opRate = Math.round((cat.operational_units / cat.total_units) * 100);
          return (
            <div
              key={cat.category}
              className="bg-slate-800/30 border border-slate-700/50 rounded-xl p-4 hover:border-slate-600 transition-all"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <span className="font-semibold text-slate-200 text-sm">{cat.category}</span>
                <span className="text-xs text-slate-400">
                  {cat.operational_units} / {cat.total_units} Operational ({opRate}%)
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs mt-3 pt-2 border-t border-slate-800/60">
                <div>
                  <span className="text-slate-400">Coverage:</span>
                  <span className="font-bold text-sky-300 ml-2">{cat.average_coverage}%</span>
                </div>
                <div>
                  <span className="text-slate-400">Quality Score:</span>
                  <span className="font-bold text-indigo-300 ml-2">{cat.average_quality}</span>
                </div>
                <div>
                  <span className="text-slate-400">Total Capacity:</span>
                  <span className="font-bold text-slate-200 ml-2">{cat.total_capacity.toLocaleString()}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
