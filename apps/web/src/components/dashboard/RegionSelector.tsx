import type { Region } from "../../types/dashboard";

interface RegionSelectorProps {
  regions: Region[];
  selectedRegionId: number | "all" | null;
  onChange: (regionId: number | "all") => void;
  disabled?: boolean;
}

export default function RegionSelector({
  regions,
  selectedRegionId,
  onChange,
  disabled = false,
}: RegionSelectorProps) {
  return (
    <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
      <label
        htmlFor="region-selector"
        className="text-sm font-medium text-slate-700"
      >
        Region
      </label>

      <select
        id="region-selector"
        value={selectedRegionId === null ? "" : selectedRegionId}
        onChange={(event) => {
          const value = event.target.value;

          if (value === "all") {
            onChange("all");
            return;
          }

          onChange(Number(value));
        }}
        disabled={disabled || regions.length === 0}
        className="rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100"
      >
        <option value="all">All Regions</option>

        {regions.map((region) => (
          <option key={region.id} value={region.id}>
            {region.name}
          </option>
        ))}
      </select>
    </div>
  );
}