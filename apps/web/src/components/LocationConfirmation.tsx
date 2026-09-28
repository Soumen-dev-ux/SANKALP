import { useState, useEffect } from "react";

interface LocationConfirmationProps {
  locationText: string | null;

  onConfirm: (
    latitude: number,
    longitude: number,
    locationText: string
  ) => void;

  onSkip: () => void;
}

function LocationConfirmation({
  locationText,
  onConfirm,
  onSkip,
}: LocationConfirmationProps) {

  const [location, setLocation] = useState(locationText || "");
  const [latitude, setLatitude] = useState("22.5726");
  const [longitude, setLongitude] = useState("88.3639");
  const [detecting, setDetecting] = useState(false);
  const [detectionMessage, setDetectionMessage] = useState<string | null>(null);

  // Auto-detect browser geolocation on component mount if supported
  useEffect(() => {
    handleAutoDetect();
  }, []);

  const handleAutoDetect = () => {
    if (!navigator.geolocation) {
      setDetectionMessage("Browser geolocation not supported. Using regional default coordinates.");
      return;
    }

    setDetecting(true);
    setDetectionMessage("Detecting location via GPS...");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude.toFixed(6);
        const lng = position.coords.longitude.toFixed(6);
        setLatitude(lat);
        setLongitude(lng);

        if (!location.trim()) {
          setLocation(`GPS Location (${lat}, ${lng})`);
        }
        setDetectionMessage("Location auto-detected successfully!");
        setDetecting(false);
      },
      (error) => {
        console.warn("Geolocation warning:", error.message);
        setDetectionMessage("GPS signal unavailable. Using regional default coordinates.");
        setDetecting(false);
      },
      { timeout: 8000, enableHighAccuracy: true }
    );
  };

  const handleConfirm = () => {
    const lat = Number(latitude) || 22.5726;
    const lng = Number(longitude) || 88.3639;
    const locName = location.trim() || `Location (${lat}, ${lng})`;

    onConfirm(lat, lng, locName);
  };

  return (
    <div className="location-card">
      <span className="eyebrow">LOCATION CONFIRMATION</span>

      <h2>Where is this issue happening?</h2>

      <p>
        Confirm or auto-detect your location so SANKALP can connect your request with local development infrastructure.
      </p>

      {/* Auto-detect button */}
      <div className="mb-4">
        <button
          type="button"
          onClick={handleAutoDetect}
          disabled={detecting}
          className="secondary-button"
          style={{ width: "100%", display: "flex", itemsCenter: "center", justifyContent: "center", gap: "8px" }}
        >
          {detecting ? "📡 Detecting Location..." : "📍 Auto-Detect My GPS Location"}
        </button>
        {detectionMessage && (
          <p className="text-xs text-sky-600 mt-2 text-center font-medium">
            {detectionMessage}
          </p>
        )}
      </div>

      <label>Location description / Landmark</label>

      <input
        type="text"
        value={location}
        onChange={(event) => setLocation(event.target.value)}
        placeholder="Example: Ward 12, Salt Lake or Village Rampur"
      />

      <div className="coordinate-grid">
        <div>
          <label>Latitude</label>

          <input
            type="number"
            value={latitude}
            onChange={(event) => setLatitude(event.target.value)}
            placeholder="22.5726"
            step="any"
          />
        </div>

        <div>
          <label>Longitude</label>

          <input
            type="number"
            value={longitude}
            onChange={(event) => setLongitude(event.target.value)}
            placeholder="88.3639"
            step="any"
          />
        </div>
      </div>

      <div className="location-actions">
        <button className="secondary-button" onClick={onSkip}>
          Skip for now
        </button>

        <button className="primary-button" onClick={handleConfirm}>
          Confirm Location →
        </button>
      </div>
    </div>
  );
}

export default LocationConfirmation;