import { useEffect } from "react";
import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import type {
  CitizenRequestLocation,
  GovernmentProject,
  InfrastructureRecord,
} from "../../types/dashboard";

import "leaflet/dist/leaflet.css";

interface IntelligenceMapProps {
  infrastructure: InfrastructureRecord[];
  projects: GovernmentProject[];
  requests: CitizenRequestLocation[];
}

interface MapBoundsProps {
  points: [number, number][];
}

function MapBounds({ points }: MapBoundsProps) {
  const map = useMap();

  useEffect(() => {
    if (points.length === 0) {
      return;
    }

    if (points.length === 1) {
      map.setView(points[0], 13);
      return;
    }

    const bounds = points.map(
      ([latitude, longitude]) => [latitude, longitude] as [number, number]
    );

    map.fitBounds(bounds, {
      padding: [40, 40],
    });
  }, [map, points]);

  return null;
}

export default function IntelligenceMap({
  infrastructure,
  projects,
  requests,
}: IntelligenceMapProps) {
  const infrastructurePoints = infrastructure.filter(
    (item) => item.latitude !== null && item.longitude !== null
  );

  const projectPoints = projects.filter(
    (item) => item.latitude !== null && item.longitude !== null
  );

  const requestPoints = requests.filter(
    (item) => item.latitude !== null && item.longitude !== null
  );

  const points: [number, number][] = [
    ...infrastructurePoints.map(
      (item) => [item.latitude!, item.longitude!] as [number, number]
    ),
    ...projectPoints.map(
      (item) => [item.latitude!, item.longitude!] as [number, number]
    ),
    ...requestPoints.map(
      (item) => [item.latitude!, item.longitude!] as [number, number]
    ),
  ];

  const defaultCenter: [number, number] = [22.5726, 88.3639];

  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <div className="h-[520px] w-full">
        <MapContainer
          center={defaultCenter}
          zoom={11}
          scrollWheelZoom
          className="h-full w-full"
        >
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapBounds points={points} />

          {/* Infrastructure */}
          {infrastructurePoints.map((item) => (
            <CircleMarker
              key={`infra-${item.id}`}
              center={[item.latitude!, item.longitude!]}
              radius={9}
              pathOptions={{
                color: "#2563eb",
                fillColor: "#3b82f6",
                fillOpacity: 0.75,
              }}
            >
              <Popup>
                <div className="space-y-1">
                  <h3 className="font-semibold">
                    {item.name || item.infrastructure_type}
                  </h3>

                  <p>
                    <strong>Type:</strong>{" "}
                    {item.infrastructure_type}
                  </p>

                  <p>
                    <strong>Category:</strong> {item.category}
                  </p>

                  <p>
                    <strong>Operational:</strong>{" "}
                    {item.operational ? "Yes" : "No"}
                  </p>

                  {item.coverage_percent !== null && (
                    <p>
                      <strong>Coverage:</strong>{" "}
                      {item.coverage_percent}%
                    </p>
                  )}

                  {item.quality_score !== null && (
                    <p>
                      <strong>Quality:</strong>{" "}
                      {item.quality_score}
                    </p>
                  )}
                </div>
              </Popup>
            </CircleMarker>
          ))}

          {/* Government projects */}
          {projectPoints.map((project) => (
            <CircleMarker
              key={`project-${project.id}`}
              center={[project.latitude!, project.longitude!]}
              radius={10}
              pathOptions={{
                color: "#7c3aed",
                fillColor: "#8b5cf6",
                fillOpacity: 0.8,
              }}
            >
              <Popup>
                <div className="space-y-1">
                  <h3 className="font-semibold">
                    {project.name}
                  </h3>

                  <p>
                    <strong>Category:</strong>{" "}
                    {project.category}
                  </p>

                  <p>
                    <strong>Status:</strong>{" "}
                    {project.status}
                  </p>

                  {project.implementing_agency && (
                    <p>
                      <strong>Agency:</strong>{" "}
                      {project.implementing_agency}
                    </p>
                  )}

                  {project.budget !== null && (
                    <p>
                      <strong>Budget:</strong>{" "}
                      ₹{project.budget.toLocaleString("en-IN")}
                    </p>
                  )}
                </div>
              </Popup>
            </CircleMarker>
          ))}

          {/* Citizen requests */}
          {requestPoints.map((request) => (
            <CircleMarker
              key={`request-${request.id}`}
              center={[request.latitude!, request.longitude!]}
              radius={7}
              pathOptions={{
                color: "#dc2626",
                fillColor: "#ef4444",
                fillOpacity: 0.7,
              }}
            >
              <Popup>
                <div className="space-y-1">
                  <h3 className="font-semibold">
                    Citizen Request
                  </h3>

                  <p>
                    <strong>Reference:</strong>{" "}
                    {request.anonymous_reference}
                  </p>

                  {request.category && (
                    <p>
                      <strong>Category:</strong>{" "}
                      {request.category}
                    </p>
                  )}

                  <p>
                    <strong>Status:</strong>{" "}
                    {request.status}
                  </p>

                  <p className="mt-2 text-sm">
                    {request.raw_text}
                  </p>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-5 border-t border-slate-200 px-5 py-4 text-sm">
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-blue-500" />
          <span>Infrastructure</span>
        </div>

        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-violet-500" />
          <span>Government Project</span>
        </div>

        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-red-500" />
          <span>Citizen Request</span>
        </div>
      </div>
    </div>
  );
}