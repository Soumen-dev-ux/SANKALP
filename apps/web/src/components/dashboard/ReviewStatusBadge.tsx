interface ReviewStatusBadgeProps {
  status: string;
}

export default function ReviewStatusBadge({
  status,
}: ReviewStatusBadgeProps) {
  const labels: Record<string, string> = {
    not_required: "No Review Required",
    pending: "Human Review Pending",
    approved: "Human Reviewed",
    corrected: "Human Corrected",
  };

  return (
    <span className="inline-flex rounded-full border px-3 py-1 text-xs font-medium">
      {labels[status] ?? "Review Status Unknown"}
    </span>
  );
}