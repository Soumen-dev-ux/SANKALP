import React, { useState } from "react";
import type { RegionalTrends } from "../../types/intelligence";

interface Props {
  data: RegionalTrends | null;
  loading: boolean;
  onIntervalChange: (interval: "daily" | "weekly" | "monthly") => void;
}

export const IntelligenceTrendsChart: React.FC<Props> = ({
  data,
  loading,
  onIntervalChange,
}) => {
  const [selectedInterval, setSelectedInterval] = useState<"daily" | "weekly" | "monthly">("monthly");

  const handleIntervalClick = (interval: "daily" | "weekly" | "monthly") => {
    setSelectedInterval(interval);
    onIntervalChange(interval);
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse bg-slate-900/60 rounded-2xl border border-slate-800">
        Loading trend & time-series analysis...
      </div>
    );
  }

  const trends = data?.trends || [];
  const maxVal = Math.max(...trends.map((t) => t.total_requests), 1);

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="text-sky-400">📈</span> Citizen Demand Trends & Time-Series
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Track demand velocity over time aggregated by date intervals.
          </p>
        </div>

        {/* Interval Selector */}
        <div className="flex items-center bg-slate-800/80 p-1 rounded-xl border border-slate-700">
          {(["daily", "weekly", "monthly"] as const).map((intv) => (
            <button
              key={intv}
              onClick={() => handleIntervalClick(intv)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg capitalize transition-all ${
                selectedInterval === intv
                  ? "bg-sky-500 text-white shadow-md shadow-sky-500/20"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {intv}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Ribbon */}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50 flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Growth Rate</span>
            <span
              className={`text-base font-bold ${
                data.growth_rate_percent >= 0 ? "text-emerald-400" : "text-rose-400"
              }`}
            >
              {data.growth_rate_percent >= 0 ? "+" : ""}
              {data.growth_rate_percent}%
            </span>
          </div>

          <div className="bg-slate-800/40 p-4 rounded-xl border border-slate-700/50 flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Rising Demand Sector</span>
            <span className="text-base font-bold text-amber-300">
              {data.dominant_rising_category || "N/A"}
            </span>
          </div>
        </div>
      )}

      {/* Bar Chart Visualization */}
      {trends.length === 0 ? (
        <div className="p-8 text-center text-slate-500 text-sm">
          No time-series demand records logged for this interval.
        </div>
      ) : (
        <div className="space-y-3">
          <div className="flex items-end gap-2 h-44 pt-6 px-2 border-b border-slate-800 pb-2">
            {trends.map((point) => {
              const heightPct = Math.round((point.total_requests / maxVal) * 100);
              return (
                <div
                  key={point.timestamp}
                  className="flex-1 flex flex-col items-center gap-2 h-full justify-end group relative"
                >
                  {/* Tooltip */}
                  <div className="absolute -top-10 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-800 text-slate-100 text-[10px] px-2 py-1 rounded shadow-lg border border-slate-700 whitespace-nowrap z-10">
                    {point.timestamp}: {point.total_requests} requests
                  </div>

                  <div className="w-full max-w-[36px] bg-slate-800/80 rounded-t-lg overflow-hidden h-full flex items-end">
                    <div
                      className="w-full bg-gradient-to-t from-sky-600 to-indigo-500 rounded-t-lg transition-all duration-500 group-hover:from-sky-400 group-hover:to-indigo-400"
                      style={{ height: `${heightPct}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono rotate-45 sm:rotate-0 origin-left">
                    {point.timestamp.slice(-5)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
