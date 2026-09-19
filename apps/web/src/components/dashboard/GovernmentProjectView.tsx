import type { GovernmentProject } from "../../types/dashboard";

interface GovernmentProjectViewProps {
  projects: GovernmentProject[];
}

function formatBudget(budget: number | null) {
  if (budget === null || budget === undefined) {
    return "Not available";
  }

  return `₹${budget.toLocaleString("en-IN")}`;
}

function formatDate(date: string | null) {
  if (!date) {
    return "Not specified";
  }

  return new Date(date).toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function getStatusClass(status: GovernmentProject["status"]) {
  switch (status) {
    case "Ongoing":
      return "bg-blue-50 text-blue-700";

    case "Completed":
      return "bg-green-50 text-green-700";

    case "Planned":
      return "bg-yellow-50 text-yellow-700";

    case "Cancelled":
      return "bg-red-50 text-red-700";

    default:
      return "bg-gray-50 text-gray-700";
  }
}

export default function GovernmentProjectView({
  projects,
}: GovernmentProjectViewProps) {
  if (projects.length === 0) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center shadow-sm">
        <h3 className="font-semibold text-gray-900">
          No government projects found
        </h3>

        <p className="mt-2 text-sm text-gray-500">
          There are currently no project records available for
          this region.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {projects.map((project) => (
        <article
          key={project.id}
          className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm"
        >
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
            <div className="min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="text-lg font-semibold text-gray-900">
                  {project.name}
                </h3>

                <span
                  className={`rounded-full px-2.5 py-1 text-xs font-medium ${getStatusClass(
                    project.status
                  )}`}
                >
                  {project.status}
                </span>
              </div>

              <p className="mt-2 text-sm font-medium text-gray-600">
                {project.category}
              </p>

              {project.description && (
                <p className="mt-2 text-sm leading-6 text-gray-500">
                  {project.description}
                </p>
              )}
            </div>

            <div className="shrink-0 rounded-lg bg-gray-50 px-4 py-3">
              <p className="text-xs text-gray-500">
                Budget
              </p>

              <p className="mt-1 font-semibold text-gray-900">
                {formatBudget(project.budget)}
              </p>
            </div>
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 border-t border-gray-100 pt-5 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <p className="text-xs text-gray-500">
                Implementing Agency
              </p>

              <p className="mt-1 text-sm font-medium text-gray-800">
                {project.implementing_agency ?? "Not specified"}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">
                Start Date
              </p>

              <p className="mt-1 text-sm font-medium text-gray-800">
                {formatDate(project.start_date)}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">
                Expected Completion
              </p>

              <p className="mt-1 text-sm font-medium text-gray-800">
                {formatDate(project.expected_completion_date)}
              </p>
            </div>

            <div>
              <p className="text-xs text-gray-500">
                Location
              </p>

              <p className="mt-1 text-sm font-medium text-gray-800">
                {project.latitude !== null &&
                project.longitude !== null
                  ? `${project.latitude.toFixed(
                      4
                    )}, ${project.longitude.toFixed(4)}`
                  : "Not specified"}
              </p>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}