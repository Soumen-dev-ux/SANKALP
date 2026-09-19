import type { RegionSummary } from "../../types/dashboard";

interface RegionalSummaryCardsProps {
  summary: RegionSummary | null;
}

export default function RegionalSummaryCards({
  summary,
}: RegionalSummaryCardsProps) {
  if (!summary) {
    return null;
  }

  const cards = [
    {
      label: "Citizen Requests",
      value: summary.request_count,
      icon: "📣",
      accent: "from-blue-500/10 via-blue-500/5 to-transparent",
      borderColor: "border-blue-200/80",
    },
    {
      label: "Infrastructure",
      value: summary.infrastructure_count,
      icon: "🏗️",
      accent: "from-amber-500/10 via-amber-500/5 to-transparent",
      borderColor: "border-amber-200/80",
    },
    {
      label: "Government Projects",
      value: summary.project_count,
      icon: "🎯",
      accent: "from-purple-500/10 via-purple-500/5 to-transparent",
      borderColor: "border-purple-200/80",
    },
    {
      label: "Demographic Records",
      value: summary.demographics_count,
      icon: "📊",
      accent: "from-emerald-500/10 via-emerald-500/5 to-transparent",
      borderColor: "border-emerald-200/80",
    },
  ];

  return (
    <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      {cards.map((card) => (
        <div
          key={card.label}
          className={`group relative overflow-hidden rounded-2xl border ${card.borderColor} bg-white p-5 shadow-xs hover:shadow-md hover:-translate-y-0.5 transition-all duration-300`}
        >
          <div className={`absolute inset-0 bg-gradient-to-br ${card.accent} opacity-50 group-hover:opacity-100 transition-opacity`} />

          <div className="relative flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
              {card.label}
            </p>
            <span className="text-xl group-hover:scale-110 transition-transform duration-300">
              {card.icon}
            </span>
          </div>

          <div className="relative mt-3 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold tracking-tight text-slate-900">
              {card.value.toLocaleString()}
            </span>
            <span className="text-xs font-medium text-slate-400">records</span>
          </div>
        </div>
      ))}
    </div>
  );
}