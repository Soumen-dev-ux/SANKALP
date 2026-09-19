export default function DashboardDisclaimer() {
  return (
    <div className="mt-8 rounded-xl border border-blue-100 bg-blue-50 p-5">
      <h3 className="text-sm font-semibold text-blue-900">
        About these insights
      </h3>

      <p className="mt-2 text-sm leading-6 text-blue-800">
        SANKALP development insights are analytical indicators
        generated from available citizen requests, infrastructure
        records, demographic context, and project data. They are
        intended to support human review and do not replace
        official verification, feasibility assessment, budgeting,
        or administrative decisions.
      </p>

      <p className="mt-2 text-xs text-blue-700">
        Current dashboard records may include synthetic demo data
        for platform demonstration.
      </p>
    </div>
  );
}