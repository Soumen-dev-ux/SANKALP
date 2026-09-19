import { useState } from "react";

import CitizenRequestForm from "./components/CitizenRequestForm";
import AnalysisResult from "./components/AnalysisResult";
import SubmissionSuccess from "./components/SubmissionSuccess"
import api from "./services/api";
import LocationConfirmation from "./components/LocationConfirmation";

import type {
  CitizenAnalysis,
  CitizenRequestResponse,
} from "./types/citizenRequest";

import "./App.css";

type AppStep =
  | "input"
  | "analysis"
  | "location"
  | "success";

function App() {
  const [step, setStep] =
    useState<AppStep>("input");

  const [analysis, setAnalysis] =
    useState<CitizenAnalysis | null>(null);

  const [originalText, setOriginalText] =
    useState("");

  const [reference, setReference] =
    useState("");

  const [locationText, setLocationText] =
    useState<string | null>(null);

  const [, setLatitude] =
    useState<number | null>(null);

  const [, setLongitude] =
    useState<number | null>(null);

  const [inputSource, setInputSource] =
    useState<"web" | "voice">("web");

  const handleAnalysisComplete = (
    result: CitizenAnalysis,
    text: string,
    source: "web" | "voice"
  ) => {
    setAnalysis(result);
    setOriginalText(text);
    setInputSource(source);
    setStep("analysis");
  };

  const handleAnalysisConfirm = () => {
    if (!analysis) {
      return;
    }

    setLocationText(
      analysis.location_text
    );

    setStep("location");
  };

  const handleLocationConfirm = async (
    lat: number,
    lng: number,
    location: string
  ) => {
    setLatitude(lat);
    setLongitude(lng);
    setLocationText(location);

    await submitRequest(
      lat,
      lng
    );
  };

  const handleSkipLocation = async () => {
    await submitRequest(null, null);
  };

  const submitRequest = async (
    lat: number | null,
    lng: number | null
  ) => {
    if (!analysis) {
      return;
    }

    try {
      const response =
        await api.post<CitizenRequestResponse>(
          "/requests",
          {
            raw_text: originalText,

            language: analysis.language,
            category: analysis.category,
            intent: analysis.intent,
            issue: analysis.issue,

            latitude: lat,
            longitude: lng,

            source: inputSource,
          }
        );

      setReference(
        response.data.anonymous_reference
      );

      setStep("success");

    } catch (error) {
      console.error(
        "Failed to submit request:",
        error
      );

      alert(
        "Unable to submit the request. Please try again."
      );
    }
  };

  const handleEdit = () => {
    setStep("input");
  };

  const handleCreateAnother = () => {
    setAnalysis(null);
    setOriginalText("");
    setReference("");
    setStep("input");
  };

  return (
    <div className="app">

      <header className="navbar">

        <div className="brand">
          <div className="brand-mark">
            S
          </div>

          <div>
            <strong>SANKALP</strong>

            <span>
              Citizen Development Intelligence
            </span>
          </div>
        </div>

        <div className="language-indicator">
          EN · বাংলা · हिन्दी
        </div>

      </header>

      <main className="main-content">

        <div className="progress">

          <div
            className={
              step === "input"
                ? "progress-step active"
                : "progress-step"
            }
          >
            1. Tell us
          </div>

          <div
            className={
              step === "analysis"
                ? "progress-step active"
                : "progress-step"
            }
          >
            2. Review
          </div>

          <div
            className={
              step === "location"
                ? "progress-step active"
                : "progress-step"
            }
          >
            3. Location
          </div>

          <div
            className={
              step === "success"
                ? "progress-step active"
                : "progress-step"
            }
          >
            4. Submitted
          </div>

        </div>

        {step === "input" && (
          <CitizenRequestForm
            onAnalysisComplete={
              handleAnalysisComplete
            }
          />
        )}

        {step === "analysis" &&
          analysis && (
            <AnalysisResult
              analysis={analysis}
              originalText={originalText}
              onConfirm={handleAnalysisConfirm}
              onEdit={handleEdit}
            />
          )}

        {step === "location" && (
          <LocationConfirmation
            locationText={locationText}
            onConfirm={handleLocationConfirm}
            onSkip={handleSkipLocation}
          />
        )}

        {step === "success" && (
          <SubmissionSuccess
            reference={reference}
            onCreateAnother={
              handleCreateAnother
            }
          />
        )}

      </main>

      <footer className="footer">
        SANKALP · Listen. Understand. Prioritize.
        Develop.
      </footer>

    </div>
  );
}

export default App;