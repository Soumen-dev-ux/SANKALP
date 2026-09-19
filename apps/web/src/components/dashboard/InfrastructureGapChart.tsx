import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import type { RegionalInfrastructureGap } from "../../types/dashboard";

interface InfrastructureGapChartProps {
  infrastructureGap: RegionalInfrastructureGap | null;
}

export default function InfrastructureGapChart({
  infrastructureGap,
}: InfrastructureGapChartProps) {
  if (
    !infrastructureGap ||
    infrastructureGap.categories.length === 0
  ) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center">
        <p className="text-gray-500">
          No infrastructure gap data available for this region.
        </p>
      </div>
    );
  }

  const chartData = infrastructureGap.categories.map((item) => ({
    category: item.category,
    demand: Number(item.demand_score.toFixed(1)),
    coverage: Number(item.infrastructure_coverage.toFixed(1)),
    gap: Number(item.gap_score.toFixed(1)),
  }));

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900">
          Infrastructure Gap Analysis
        </h3>

        <p className="mt-1 text-sm text-gray-500">
          Comparison between citizen demand and existing
          infrastructure coverage.
        </p>
      </div>

      <div className="h-[380px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{
              top: 10,
              right: 20,
              left: 0,
              bottom: 70,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="category"
              angle={-35}
              textAnchor="end"
              interval={0}
              height={90}
            />

            <YAxis
              domain={[0, 100]}
              label={{
                value: "Score / Coverage (%)",
                angle: -90,
                position: "insideLeft",
              }}
            />

            <Tooltip />

            <Legend />

            <Bar
              dataKey="demand"
              name="Demand"
              radius={[5, 5, 0, 0]}
            />

            <Bar
              dataKey="coverage"
              name="Infrastructure Coverage"
              radius={[5, 5, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 border-t border-gray-100 pt-4">
        <p className="text-xs text-gray-500">
          Gap score is calculated by the SANKALP analytical model
          using demand and infrastructure coverage. It is an
          analytical indicator, not a policy decision.
        </p>
      </div>
    </div>
  );
}