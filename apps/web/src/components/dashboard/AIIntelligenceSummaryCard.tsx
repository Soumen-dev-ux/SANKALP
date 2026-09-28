import React, { useState } from "react";
import type { AIExplanation } from "../../types/intelligence";

interface Props {
  data: AIExplanation | null;
  loading: boolean;
  onRequestRefresh: () => void;
}

export const AIIntelligenceSummaryCard: React.FC<Props> = ({
  data,
  loading,
  onRequestRefresh,
}) => {
  const [activeTab, setActiveTab] = useState<"summary" | "evidence" | "questions">("summary");

  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse bg-slate-900/60 rounded-2xl border border-slate-800">
        Generating evidence-backed AI Intelligence explanation...
      </div>
    );
  }

  if (!data) {
    return (
      <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 text-center">
        <button
          onClick={onRequestRefresh}
          className="px-4 py-2 bg-gradient-to-r from-sky-500 to-indigo-600 text-white font-semibold text-xs rounded-xl shadow-lg shadow-sky-500/20 hover:from-sky-400 hover:to-indigo-500 transition-all"
        >
          ✨ Generate AI Intelligence Explanation
        </button>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-b from-slate-900/90 to-slate-900/60 border border-indigo-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-md relative overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20 text-lg">
            🤖
          </span>
          <div>
            <h3 className="text-xl font-bold text-slate-100">AI Intelligence & Guarded Narrative</h3>
            <p className="text-xs text-slate-400">
              Strictly grounded on empirical indicators. No hallucinated figures.
            </p>
          </div>
        </div>

        <button
          onClick={onRequestRefresh}
          className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold rounded-lg border border-slate-700 transition-all"
        >
          🔄 Refresh Explanation
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 mb-4 gap-4">
        {(["summary", "evidence", "questions"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-2 text-xs font-bold capitalize transition-all border-b-2 ${
              activeTab === tab
                ? "border-indigo-400 text-indigo-300"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            {tab === "summary" ? "Executive Summary" : tab === "evidence" ? "Key Evidence" : "Human Review Questions"}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="text-sm text-slate-300 space-y-3 min-h-[120px]">
        {activeTab === "summary" && (
          <div className="space-y-3 leading-relaxed bg-slate-800/30 p-4 rounded-xl border border-slate-700/40">
            <p className="text-slate-200">{data.summary}</p>
            {data.observed_trends.length > 0 && (
              <div className="pt-2 border-t border-slate-800 text-xs text-amber-300 font-medium">
                ⚡ Observed Trend: {data.observed_trends.join(" ")}
              </div>
            )}
          </div>
        )}

        {activeTab === "evidence" && (
          <ul className="space-y-2 text-xs">
            {data.key_evidence.map((ev, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-slate-800/40 p-3 rounded-lg border border-slate-700/50">
                <span className="text-emerald-400">✓</span>
                <span className="text-slate-300">{ev}</span>
              </li>
            ))}
          </ul>
        )}

        {activeTab === "questions" && (
          <ul className="space-y-2 text-xs">
            {data.questions_for_human_review.map((q, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-slate-800/40 p-3 rounded-lg border border-slate-700/50">
                <span className="text-amber-400">❓</span>
                <span className="text-slate-200 font-medium">{q}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Limitations Disclaimer */}
      {data.data_limitations.length > 0 && (
        <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-500 flex items-center gap-1.5">
          <span>⚠️ Data Limitations:</span>
          <span>{data.data_limitations.join("; ")}</span>
        </div>
      )}
    </div>
  );
};
