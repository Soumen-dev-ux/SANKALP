import React from "react";
import type { RegionalHotspots } from "../../types/intelligence";

interface Props {
  data: RegionalHotspots | null;
  loading: boolean;
}

export const HotspotMapView: React.FC<Props> = ({ data, loading }) => {
  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse bg-slate-900/60 rounded-2xl border border-slate-800">
        Detecting geographic hotspots & request clusters...
      </div>
    );
  }

  if (!data || data.total_hotspots === 0) {
    return (
      <div className="p-6 text-center text-slate-400 bg-slate-800/40 rounded-xl border border-slate-700/50">
        No geographic hotspots detected for this region.
      </div>
    );
  }

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <span className="text-rose-400">📍</span> Geographic Hotspot Intelligence
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Aggregated spatial grouping protecting exact citizen coordinates.
          </p>
        </div>
        <span className="px-3 py-1 bg-rose-500/10 text-rose-300 text-xs font-semibold rounded-full border border-rose-500/20">
          {data.total_hotspots} Hotspots Found
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {data.hotspots.map((spot) => (
          <div
            key={spot.hotspot_id}
            className="bg-slate-800/40 border border-slate-700/50 rounded-xl p-4 hover:border-slate-600 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold font-mono text-rose-400 text-sm">{spot.hotspot_id}</span>
                <span className="px-2 py-0.5 bg-slate-900/60 text-slate-300 text-xs rounded border border-slate-700">
                  ~{spot.radius_km} km radius
                </span>
              </div>

              <div className="text-xs text-slate-300 space-y-1 mb-3">
                <p>
                  <span className="text-slate-500">Approx. Center:</span> {spot.approx_latitude}° N, {spot.approx_longitude}° E
                </p>
                <p>
                  <span className="text-slate-500">Total Requests:</span> <strong className="text-sky-300">{spot.request_count}</strong>
                </p>
                <p>
                  <span className="text-slate-500">Dominant Category:</span> <strong className="text-amber-300">{spot.dominant_category}</strong>
                </p>
              </div>
            </div>

            {/* Category Pill Breakdown */}
            <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-800/60">
              {Object.entries(spot.categories).map(([cat, count]) => (
                <span
                  key={cat}
                  className="px-2 py-0.5 bg-slate-900/80 text-[10px] text-slate-400 rounded-md border border-slate-800"
                >
                  {cat}: <strong className="text-slate-200">{count}</strong>
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
