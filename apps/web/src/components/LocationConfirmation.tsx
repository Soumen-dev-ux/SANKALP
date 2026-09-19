import { useState } from "react";

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

  const [location, setLocation] =
    useState(locationText || "");

  const [latitude, setLatitude] =
    useState("");

  const [longitude, setLongitude] =
    useState("");

  const handleConfirm = () => {

    const lat = Number(latitude);
    const lng = Number(longitude);

    if (
      !location.trim() ||
      Number.isNaN(lat) ||
      Number.isNaN(lng)
    ) {
      return;
    }

    onConfirm(
      lat,
      lng,
      location.trim()
    );
  };

  return (
    <div className="location-card">

      <span className="eyebrow">
        LOCATION
      </span>

      <h2>
        Where is this issue happening?
      </h2>

      <p>
        Confirm the location so SANKALP can
        connect your request with local
        development data.
      </p>

      <label>
        Location description
      </label>

      <input
        type="text"
        value={location}
        onChange={(event) =>
          setLocation(event.target.value)
        }
        placeholder="Example: Ward 12, Salt Lake"
      />

      <div className="coordinate-grid">

        <div>
          <label>
            Latitude
          </label>

          <input
            type="number"
            value={latitude}
            onChange={(event) =>
              setLatitude(event.target.value)
            }
            placeholder="22.5726"
            step="any"
          />
        </div>

        <div>
          <label>
            Longitude
          </label>

          <input
            type="number"
            value={longitude}
            onChange={(event) =>
              setLongitude(event.target.value)
            }
            placeholder="88.3639"
            step="any"
          />
        </div>

      </div>

      <div className="location-actions">

        <button
          className="secondary-button"
          onClick={onSkip}
        >
          Skip for now
        </button>

        <button
          className="primary-button"
          onClick={handleConfirm}
        >
          Confirm Location →
        </button>

      </div>

    </div>
  );
}

export default LocationConfirmation;