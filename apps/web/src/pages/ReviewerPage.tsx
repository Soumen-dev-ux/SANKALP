import React, { useState, useEffect } from "react";
import {
  getPendingReviews,
  submitReviewAction,
  getReviewHistory,
  type PendingReview,
  type ReviewAction,
} from "../services/api";

export default function ReviewerPage() {
  const [pendingQueue, setPendingQueue] = useState<PendingReview[]>([]);
  const [selectedRequest, setSelectedRequest] = useState<PendingReview | null>(null);
  const [history, setHistory] = useState<ReviewAction[]>([]);
  
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterCategory, setFilterCategory] = useState<string>("all");

  // Review Form State
  const [actionStatus, setActionStatus] = useState<"approved" | "corrected">("approved");
  const [reviewerNote, setReviewerNote] = useState("");
  const [reviewedCategory, setReviewedCategory] = useState("");
  const [reviewedIssue, setReviewedIssue] = useState("");
  const [reviewedLocation, setReviewedLocation] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    fetchQueue();
  }, []);

  useEffect(() => {
    if (selectedRequest) {
      setReviewedCategory(selectedRequest.category || "");
      setReviewedIssue(selectedRequest.issue || "");
      setReviewedLocation(selectedRequest.location_text || "");
      setActionStatus("approved");
      setReviewerNote("");
      setFeedbackMessage(null);
      fetchHistory(selectedRequest.request_id);
    }
  }, [selectedRequest]);

  const fetchQueue = async () => {
    setIsLoading(true);
    try {
      const data = await getPendingReviews();
      setPendingQueue(data);
      if (data.length > 0 && !selectedRequest) {
        setSelectedRequest(data[0]);
      }
    } catch (err) {
      console.error("Failed to load review queue:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchHistory = async (requestId: number) => {
    try {
      const logs = await getReviewHistory(requestId);
      setHistory(logs);
    } catch (err) {
      console.error("Failed to fetch review history:", err);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRequest) return;

    setIsSubmitting(true);
    setFeedbackMessage(null);

    try {
      await submitReviewAction(selectedRequest.request_id, {
        status: actionStatus,
        reviewer_note: reviewerNote || null,
        reviewed_category: actionStatus === "corrected" ? reviewedCategory : undefined,
        reviewed_issue: actionStatus === "corrected" ? reviewedIssue : undefined,
        reviewed_location: actionStatus === "corrected" ? reviewedLocation : undefined,
      });

      setFeedbackMessage({
        type: "success",
        text: `Review submitted successfully! Request set to ${actionStatus}.`,
      });

      // Refresh queue and history
      const updatedQueue = pendingQueue.filter((r) => r.request_id !== selectedRequest.request_id);
      setPendingQueue(updatedQueue);
      if (updatedQueue.length > 0) {
        setSelectedRequest(updatedQueue[0]);
      } else {
        setSelectedRequest(null);
      }
    } catch (err: any) {
      console.error("Failed to submit review action:", err);
      const msg = err.response?.data?.error?.message || "Failed to submit review. Please try again.";
      setFeedbackMessage({ type: "error", text: msg });
    } finally {
      setIsSubmitting(false);
    }
  };

  const filteredQueue = pendingQueue.filter((item) => {
    const matchesSearch =
      item.anonymous_reference.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.raw_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (item.category && item.category.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesCategory = filterCategory === "all" || item.category === filterCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = Array.from(new Set(pendingQueue.map((i) => i.category).filter(Boolean)));

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Top Header */}
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold tracking-tight text-slate-900">
              Human Reviewer Portal
            </h1>
            <span className="rounded-full bg-blue-100 px-3 py-0.5 text-xs font-semibold text-blue-700">
              Phase 6.3 Security Enforced
            </span>
          </div>
          <p className="mt-1 text-xs font-medium text-slate-500">
            Inspect AI classifications, verify flagged submissions, and maintain authoritative records.
          </p>
        </div>

        <button
          onClick={fetchQueue}
          disabled={isLoading}
          className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 active:scale-95 transition-all cursor-pointer"
        >
          <svg className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh Queue
        </button>
      </div>

      {/* Queue Stat Overview Cards */}
      <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm">
          <div className="text-xs font-medium uppercase tracking-wider text-slate-400">Total Pending Reviews</div>
          <div className="mt-2 text-3xl font-extrabold text-slate-900">{pendingQueue.length}</div>
        </div>
        <div className="rounded-2xl border border-amber-200/80 bg-amber-50/40 p-5 shadow-sm">
          <div className="text-xs font-medium uppercase tracking-wider text-amber-700">AI Confidence Flagged</div>
          <div className="mt-2 text-3xl font-extrabold text-amber-900">
            {pendingQueue.filter((i) => i.confidence_review_required).length}
          </div>
        </div>
        <div className="rounded-2xl border border-emerald-200/80 bg-emerald-50/40 p-5 shadow-sm">
          <div className="text-xs font-medium uppercase tracking-wider text-emerald-700">System Status</div>
          <div className="mt-2 text-sm font-bold text-emerald-900 flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            RBAC & Security Active
          </div>
        </div>
      </div>

      {/* Main Workspace Grid */}
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-12">
        {/* Left Column: Review Queue List */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex flex-col gap-3 rounded-2xl border border-slate-200/80 bg-white p-4 shadow-sm">
            <div className="relative">
              <input
                type="text"
                placeholder="Search reference or description..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2 text-xs text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none transition-all"
              />
            </div>
            
            {categories.length > 0 && (
              <div className="flex gap-1 overflow-x-auto pb-1">
                <button
                  onClick={() => setFilterCategory("all")}
                  className={`rounded-lg px-2.5 py-1 text-[11px] font-semibold whitespace-nowrap transition-all ${
                    filterCategory === "all" ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  All ({pendingQueue.length})
                </button>
                {categories.map((cat) => (
                  <button
                    key={cat!}
                    onClick={() => setFilterCategory(cat!)}
                    className={`rounded-lg px-2.5 py-1 text-[11px] font-semibold whitespace-nowrap transition-all ${
                      filterCategory === cat ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Queue List */}
          <div className="space-y-3 max-h-[620px] overflow-y-auto pr-1">
            {isLoading ? (
              <div className="rounded-2xl border border-slate-200 bg-white p-8 text-center text-xs text-slate-400">
                Loading pending reviews...
              </div>
            ) : filteredQueue.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-200 bg-white p-8 text-center text-xs text-slate-500">
                No pending requests match your filter.
              </div>
            ) : (
              filteredQueue.map((item) => {
                const isSelected = selectedRequest?.request_id === item.request_id;
                return (
                  <div
                    key={item.request_id}
                    onClick={() => setSelectedRequest(item)}
                    className={`group relative rounded-2xl border p-4 transition-all cursor-pointer ${
                      isSelected
                        ? "border-blue-500 bg-blue-50/40 shadow-md ring-1 ring-blue-500/20"
                        : "border-slate-200/80 bg-white hover:border-slate-300 hover:shadow-sm"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-slate-900">
                        {item.anonymous_reference}
                      </span>
                      {item.confidence_review_required && (
                        <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-semibold text-amber-700">
                          Review Required
                        </span>
                      )}
                    </div>

                    <p className="mt-2 line-clamp-2 text-xs text-slate-600">
                      "{item.raw_text}"
                    </p>

                    <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400">
                      <span className="rounded-md bg-slate-100 px-2 py-0.5 font-medium text-slate-600">
                        {item.category || "Unclassified"}
                      </span>
                      <span>{new Date(item.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Column: Detailed Request Inspection & Action Panel */}
        <div className="lg:col-span-7">
          {selectedRequest ? (
            <div className="space-y-6">
              {/* Request Info Card */}
              <div className="rounded-3xl border border-slate-200/80 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                  <div>
                    <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                      Citizen Request Reference
                    </span>
                    <h2 className="text-xl font-mono font-bold text-slate-900">
                      {selectedRequest.anonymous_reference}
                    </h2>
                  </div>
                  <span className="rounded-full bg-blue-50 border border-blue-200 px-3 py-1 text-xs font-semibold text-blue-700">
                    Status: {selectedRequest.review_status}
                  </span>
                </div>

                {/* Raw Text Submission */}
                <div className="mt-4">
                  <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                    Citizen Submission
                  </span>
                  <div className="mt-1.5 rounded-2xl bg-slate-50 border border-slate-200/80 p-4 text-sm leading-relaxed text-slate-800">
                    "{selectedRequest.raw_text}"
                  </div>
                </div>

                {/* AI Extracted Attributes */}
                <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-3">
                  <div className="rounded-xl border border-slate-200/60 bg-slate-50/50 p-3">
                    <div className="text-[10px] font-semibold uppercase text-slate-400">AI Category</div>
                    <div className="mt-1 text-xs font-bold text-slate-800">{selectedRequest.category || "N/A"}</div>
                  </div>
                  <div className="rounded-xl border border-slate-200/60 bg-slate-50/50 p-3">
                    <div className="text-[10px] font-semibold uppercase text-slate-400">AI Issue</div>
                    <div className="mt-1 text-xs font-bold text-slate-800">{selectedRequest.issue || "N/A"}</div>
                  </div>
                  <div className="rounded-xl border border-slate-200/60 bg-slate-50/50 p-3">
                    <div className="text-[10px] font-semibold uppercase text-slate-400">AI Location</div>
                    <div className="mt-1 text-xs font-bold text-slate-800">{selectedRequest.location_text || "N/A"}</div>
                  </div>
                </div>
              </div>

              {/* Reviewer Action Form */}
              <div className="rounded-3xl border border-slate-200/80 bg-white p-6 shadow-sm">
                <h3 className="text-base font-bold text-slate-900">
                  Reviewer Decision & Actions
                </h3>
                <p className="mt-0.5 text-xs text-slate-500">
                  Select whether to approve the AI interpretation or apply manual corrections.
                </p>

                {feedbackMessage && (
                  <div className={`mt-4 rounded-xl border p-3.5 text-xs ${
                    feedbackMessage.type === "success"
                      ? "border-emerald-200 bg-emerald-50 text-emerald-800"
                      : "border-red-200 bg-red-50 text-red-800"
                  }`}>
                    {feedbackMessage.text}
                  </div>
                )}

                <form onSubmit={handleSubmitReview} className="mt-5 space-y-4">
                  {/* Status Selection */}
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setActionStatus("approved")}
                      className={`rounded-2xl border p-3 text-left transition-all cursor-pointer ${
                        actionStatus === "approved"
                          ? "border-emerald-500 bg-emerald-50/50 ring-2 ring-emerald-500/20"
                          : "border-slate-200 bg-slate-50 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span className={`h-3 w-3 rounded-full ${actionStatus === "approved" ? "bg-emerald-500" : "bg-slate-300"}`}></span>
                        <span className="text-xs font-bold text-slate-800">Approve AI Interpretation</span>
                      </div>
                      <p className="mt-1 text-[11px] text-slate-500">
                        Accept current category, issue, and location.
                      </p>
                    </button>

                    <button
                      type="button"
                      onClick={() => setActionStatus("corrected")}
                      className={`rounded-2xl border p-3 text-left transition-all cursor-pointer ${
                        actionStatus === "corrected"
                          ? "border-blue-500 bg-blue-50/50 ring-2 ring-blue-500/20"
                          : "border-slate-200 bg-slate-50 hover:bg-slate-100"
                      }`}
                    >
                      <div className="flex items-center gap-2">
                        <span className={`h-3 w-3 rounded-full ${actionStatus === "corrected" ? "bg-blue-500" : "bg-slate-300"}`}></span>
                        <span className="text-xs font-bold text-slate-800">Apply Corrections</span>
                      </div>
                      <p className="mt-1 text-[11px] text-slate-500">
                        Manually update category, issue, or location text.
                      </p>
                    </button>
                  </div>

                  {/* Editable Fields if Corrected */}
                  {actionStatus === "corrected" && (
                    <div className="space-y-3 rounded-2xl border border-blue-100 bg-blue-50/30 p-4">
                      <div>
                        <label className="block text-[11px] font-semibold uppercase text-slate-600">
                          Reviewed Category
                        </label>
                        <input
                          type="text"
                          value={reviewedCategory}
                          onChange={(e) => setReviewedCategory(e.target.value)}
                          className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-800 focus:border-blue-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-[11px] font-semibold uppercase text-slate-600">
                          Reviewed Issue
                        </label>
                        <input
                          type="text"
                          value={reviewedIssue}
                          onChange={(e) => setReviewedIssue(e.target.value)}
                          className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-800 focus:border-blue-500 focus:outline-none"
                        />
                      </div>
                      <div>
                        <label className="block text-[11px] font-semibold uppercase text-slate-600">
                          Reviewed Location
                        </label>
                        <input
                          type="text"
                          value={reviewedLocation}
                          onChange={(e) => setReviewedLocation(e.target.value)}
                          className="mt-1 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-800 focus:border-blue-500 focus:outline-none"
                        />
                      </div>
                    </div>
                  )}

                  {/* Reviewer Note */}
                  <div>
                    <label className="block text-[11px] font-semibold uppercase tracking-wider text-slate-600">
                      Reviewer Rationale & Notes
                    </label>
                    <textarea
                      rows={3}
                      value={reviewerNote}
                      onChange={(e) => setReviewerNote(e.target.value)}
                      placeholder="Add official notes regarding this verification decision..."
                      className="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50/50 p-3 text-xs text-slate-800 placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:outline-none"
                    ></textarea>
                  </div>

                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full rounded-xl bg-slate-900 py-3 text-xs font-bold text-white shadow-md hover:bg-slate-800 disabled:opacity-50 transition-all cursor-pointer"
                  >
                    {isSubmitting ? "Saving Action..." : "Commit Review Decision"}
                  </button>
                </form>
              </div>

              {/* Review History Audit Trail */}
              {history.length > 0 && (
                <div className="rounded-3xl border border-slate-200/80 bg-white p-6 shadow-sm">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                    Audit Trail & History
                  </h4>
                  <div className="mt-3 space-y-2">
                    {history.map((log) => (
                      <div key={log.id} className="rounded-xl border border-slate-100 bg-slate-50 p-3 text-xs">
                        <div className="flex items-center justify-between font-semibold text-slate-800">
                          <span>Action: {log.status}</span>
                          <span className="text-[10px] text-slate-400">
                            {new Date(log.created_at).toLocaleString()}
                          </span>
                        </div>
                        {log.reviewer_note && (
                          <p className="mt-1 text-slate-600 italic">"{log.reviewer_note}"</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex h-96 items-center justify-center rounded-3xl border border-dashed border-slate-200 bg-white text-xs text-slate-400">
              Select a request from the queue to start reviewing.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
