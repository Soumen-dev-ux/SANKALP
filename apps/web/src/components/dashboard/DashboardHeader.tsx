interface DashboardHeaderProps {
  regionName?: string;
}

export default function DashboardHeader({
  regionName,
}: DashboardHeaderProps) {
  return (
    <div className="mb-8 rounded-2xl border border-slate-200/80 bg-gradient-to-r from-white via-slate-50/50 to-blue-50/30 p-6 sm:p-8 shadow-xs">
      <div className="flex flex-wrap items-center gap-2">
        <span className="inline-flex items-center gap-1.5 rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700 border border-blue-200/60">
          <span className="h-1.5 w-1.5 rounded-full bg-blue-600 animate-pulse" />
          SANKALP Intelligence Platform
        </span>

        {regionName && (
          <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700 border border-indigo-200/60">
            Scope: <strong className="font-bold">{regionName}</strong>
          </span>
        )}
      </div>

      <h1 className="mt-3 text-2xl font-extrabold text-slate-900 sm:text-3xl lg:text-4xl tracking-tight">
        Development Intelligence Dashboard
      </h1>

      <p className="mt-2.5 max-w-3xl text-sm leading-relaxed text-slate-600 sm:text-base">
        Monitor citizen demand, infrastructure gaps, government projects,
        and regional development signals in one unified analytical workspace.
      </p>
    </div>
  );
}