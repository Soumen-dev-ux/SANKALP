import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import type { RegionalDemand } from "../../types/dashboard";

interface DemandChartProps {
  demand: RegionalDemand | null;
}

export default function DemandChart({
  demand,
}: DemandChartProps) {
  if (!demand || demand.categories.length === 0) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center">
        <p className="text-gray-500">
          No citizen demand data available for this region.
        </p>
      </div>
    );
  }

  const chartData = demand.categories.map((item) => ({
    category: item.category,
    requests: item.request_count,
    demand: item.demand_score,
  }));

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900">
          Citizen Demand by Category
        </h3>

        <p className="mt-1 text-sm text-gray-500">
          Distribution of citizen requests across development
          categories.
        </p>
      </div>

      <div className="h-[360px] w-full">
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
              allowDecimals={false}
              label={{
                value: "Requests",
                angle: -90,
                position: "insideLeft",
              }}
            />

            <Tooltip
              formatter={(value, name) => {
                if (name === "requests") {
                  return [value, "Requests"];
                }

                return [value, "Demand Score"];
              }}
            />

            <Bar
              dataKey="requests"
              name="Requests"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 border-t border-gray-100 pt-4">
        <p className="text-xs text-gray-500">
          Demand score represents the percentage share of citizen
          requests within this region.
        </p>
      </div>
    </div>
  );
}