import React, { useState } from "react";
import { downloadIntelligenceExport } from "../../services/api";

interface Props {
  regionId: number | null;
  regionName: string;
}

export const ExportReportModal: React.FC<Props> = ({ regionId, regionName }) => {
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format: "json" | "csv") => {
    try {
      setExporting(true);
      await downloadIntelligenceExport(regionId || undefined, format);
    } catch (err) {
      console.error("Export failed:", err);
      alert("Failed to export intelligence data.");
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm flex flex-wrap items-center justify-between gap-4">
      <div>
        <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <span>📥</span> Export & Intelligence Reporting
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Download structured CSV dataset or JSON intelligence payload for {regionName}.
        </p>
      </div>

      <div className="flex items-center gap-3">
        <button
          disabled={exporting}
          onClick={() => handleExport("csv")}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs rounded-xl shadow-lg shadow-emerald-600/20 transition-all flex items-center gap-1.5 disabled:opacity-50"
        >
          <span>📊</span> Export CSV
        </button>

        <button
          disabled={exporting}
          onClick={() => handleExport("json")}
          className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs rounded-xl shadow-lg shadow-sky-600/20 transition-all flex items-center gap-1.5 disabled:opacity-50"
        >
          <span>📄</span> Export JSON
        </button>
      </div>
    </div>
  );
};
