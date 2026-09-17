import { useEffect, useState } from "react";
import api from "./services/api";
import "./App.css";

type SystemStatus = {
  api: boolean;
  database: boolean;
};

function App() {
  const [status, setStatus] = useState<SystemStatus>({
    api: false,
    database: false,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSystem = async () => {
      try {
        const apiResponse = await api.get("/health/");

        const dbResponse = await api.get("/health/db");

        setStatus({
          api: apiResponse.data.status === "ok",
          database: dbResponse.data.status === "ok",
        });
      } catch (error) {
        console.error("System health check failed:", error);
      } finally {
        setLoading(false);
      }
    };

    checkSystem();
  }, []);

  return (
    <div className="app">
      <header className="navbar">
        <div>
          <h1>SANKALP</h1>
          <p>Listen. Understand. Prioritize. Develop.</p>
        </div>

        <div className="badge">
          Phase 1 · Foundation
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div>
            <span className="eyebrow">AI-POWERED DEVELOPMENT INTELLIGENCE</span>

            <h2>
              Building a smarter bridge between
              <span> citizens and development.</span>
            </h2>

            <p>
              SANKALP transforms citizen development requests into
              structured, geographically grounded intelligence for
              evidence-based planning.
            </p>
          </div>
        </section>

        <section className="status-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">SYSTEM STATUS</span>
              <h3>Foundation Infrastructure</h3>
            </div>

            <span className={loading ? "loading" : "online"}>
              {loading ? "Checking..." : "● System Check Complete"}
            </span>
          </div>

          <div className="status-grid">
            <StatusCard
              title="Frontend"
              description="React + TypeScript + Vite"
              connected={true}
            />

            <StatusCard
              title="FastAPI"
              description="Backend API service"
              connected={status.api}
            />

            <StatusCard
              title="PostgreSQL"
              description="Application database"
              connected={status.database}
            />

            <StatusCard
              title="PostGIS"
              description="Geospatial intelligence layer"
              connected={status.database}
            />
          </div>
        </section>

        <section className="architecture">
          <span className="eyebrow">CURRENT ARCHITECTURE</span>

          <div className="architecture-flow">
            <div className="architecture-card">
              <strong>Citizen</strong>
              <span>Voice / Text</span>
            </div>

            <div className="arrow">→</div>

            <div className="architecture-card">
              <strong>AI Layer</strong>
              <span>Understand</span>
            </div>

            <div className="arrow">→</div>

            <div className="architecture-card">
              <strong>API</strong>
              <span>FastAPI</span>
            </div>

            <div className="arrow">→</div>

            <div className="architecture-card">
              <strong>Data</strong>
              <span>PostgreSQL + PostGIS</span>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <p>SANKALP · Phase 1 Foundation</p>
        <p>Human oversight remains central to every development decision.</p>
      </footer>
    </div>
  );
}

type StatusCardProps = {
  title: string;
  description: string;
  connected: boolean;
};

function StatusCard({
  title,
  description,
  connected,
}: StatusCardProps) {
  return (
    <div className="status-card">
      <div className="status-icon">
        {connected ? "✓" : "!"}
      </div>

      <div>
        <h4>{title}</h4>
        <p>{description}</p>
      </div>

      <span className={connected ? "connected" : "disconnected"}>
        {connected ? "Connected" : "Offline"}
      </span>
    </div>
  );
}

export default App;