import type { RegionSummary } from "../../types/dashboard";

interface RegionalComparisonProps {
  summaries: RegionSummary[];
}

export default function RegionalComparison({
  summaries,
}: RegionalComparisonProps) {
  if (summaries.length === 0) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-6 text-center">
        <p className="text-sm text-slate-500">
          No regional data is available.
        </p>
      </div>
    );
  }

  const totalRequests = summaries.reduce(
    (sum, region) => sum + region.request_count,
    0
  );

  const totalInfrastructure = summaries.reduce(
    (sum, region) => sum + region.infrastructure_count,
    0
  );

  const totalProjects = summaries.reduce(
    (sum, region) => sum + region.project_count,
    0
  );

  return (
    <div className="space-y-6">
      {/* Overall totals */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Citizen Requests</p>
          <p className="mt-2 text-2xl font-bold text-slate-900">
            {totalRequests}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Across all regions
          </p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Infrastructure Records</p>
          <p className="mt-2 text-2xl font-bold text-slate-900">
            {totalInfrastructure}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Across all regions
          </p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Government Projects</p>
          <p className="mt-2 text-2xl font-bold text-slate-900">
            {totalProjects}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Across all regions
          </p>
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <p className="text-sm text-slate-500">Regions</p>
          <p className="mt-2 text-2xl font-bold text-slate-900">
            {summaries.length}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            With available data
          </p>
        </div>
      </div>

      {/* Regional comparison */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
        <div className="border-b border-slate-200 p-5">
          <h3 className="text-base font-semibold text-slate-900">
            Regional Data Comparison
          </h3>
          <p className="mt-1 text-sm text-slate-500">
            Compare available development records across regions.
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px] text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-5 py-3 font-medium">Region</th>
                <th className="px-5 py-3 font-medium">Requests</th>
                <th className="px-5 py-3 font-medium">Infrastructure</th>
                <th className="px-5 py-3 font-medium">Projects</th>
                <th className="px-5 py-3 font-medium">Demographics</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {summaries.map((region) => (
                <tr
                  key={region.id}
                  className="transition hover:bg-slate-50"
                >
                  <td className="px-5 py-4 font-medium text-slate-900">
                    {region.name}
                  </td>

                  <td className="px-5 py-4 text-slate-700">
                    {region.request_count}
                  </td>

                  <td className="px-5 py-4 text-slate-700">
                    {region.infrastructure_count}
                  </td>

                  <td className="px-5 py-4 text-slate-700">
                    {region.project_count}
                  </td>

                  <td className="px-5 py-4 text-slate-700">
                    {region.demographics_count}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="rounded-xl border border-blue-100 bg-blue-50 p-4">
        <p className="text-sm leading-6 text-blue-800">
          The all-region view provides descriptive comparisons of
          available records. Detailed demand, infrastructure-gap,
          project-context, and development-insight analysis is shown
          after selecting an individual region.
        </p>
      </div>
    </div>
  );
}