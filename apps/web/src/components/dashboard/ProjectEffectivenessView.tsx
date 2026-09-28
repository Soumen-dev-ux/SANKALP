import React from "react";
import type { ProjectEffectiveness } from "../../types/intelligence";

interface Props {
  data: ProjectEffectiveness | null;
  loading: boolean;
}

export const ProjectEffectivenessView: React.FC<Props> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse bg-slate-900/60 rounded-2xl border border-slate-800">
        Evaluating government project status & effectiveness...
      </div>
    );
  }

  if (!data || data.total_projects === 0) {
    return (
      <div className="p-6 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700/50">
        No government projects registered for this region.
      </div>
    );
  }

  const { status_breakdown } = data;

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="text-purple-400">🏛️</span> Government Project Effectiveness
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Status distribution and sector allocation across government initiatives.
          </p>
        </div>
        <span className="px-3 py-1 bg-purple-500/10 text-purple-300 text-xs font-semibold rounded-full border border-purple-500/20">
          {data.total_projects} Projects Logged
        </span>
      </div>

      {/* Status Badges */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-800/40 p-3 rounded-xl border border-slate-700/50 text-center">
          <span className="text-[11px] text-slate-400 uppercase font-semibold block">Planned</span>
          <span className="text-xl font-bold text-sky-400 mt-1 block">
            {status_breakdown.planned || 0}
          </span>
        </div>
        <div className="bg-slate-800/40 p-3 rounded-xl border border-slate-700/50 text-center">
          <span className="text-[11px] text-slate-400 uppercase font-semibold block">Ongoing</span>
          <span className="text-xl font-bold text-purple-400 mt-1 block">
            {status_breakdown.ongoing || 0}
          </span>
        </div>
        <div className="bg-slate-800/40 p-3 rounded-xl border border-slate-700/50 text-center">
          <span className="text-[11px] text-slate-400 uppercase font-semibold block">Completed</span>
          <span className="text-xl font-bold text-emerald-400 mt-1 block">
            {status_breakdown.completed || 0}
          </span>
        </div>
        <div className="bg-slate-800/40 p-3 rounded-xl border border-slate-700/50 text-center">
          <span className="text-[11px] text-slate-400 uppercase font-semibold block">Cancelled</span>
          <span className="text-xl font-bold text-rose-400 mt-1 block">
            {status_breakdown.cancelled || 0}
          </span>
        </div>
      </div>

      {/* Sector Alignment List */}
      <div className="space-y-3">
        {data.category_alignment.map((cat) => (
          <div
            key={cat.category}
            className="bg-slate-800/30 border border-slate-700/50 rounded-xl p-4 hover:border-slate-600 transition-all"
          >
            <div className="flex items-center justify-between gap-2 mb-2">
              <span className="font-semibold text-slate-200 text-sm">{cat.category}</span>
              <span className="text-xs font-mono text-purple-300">
                Budget: ${(cat.total_budget / 1000000).toFixed(2)}M
              </span>
            </div>

            <div className="flex items-center gap-2 text-xs text-slate-400 mt-2">
              <span className="px-2 py-0.5 bg-sky-500/10 text-sky-300 rounded border border-sky-500/20">
                {cat.planned} Planned
              </span>
              <span className="px-2 py-0.5 bg-purple-500/10 text-purple-300 rounded border border-purple-500/20">
                {cat.ongoing} Ongoing
              </span>
              <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-300 rounded border border-emerald-500/20">
                {cat.completed} Completed
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
