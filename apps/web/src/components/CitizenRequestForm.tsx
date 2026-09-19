import {
  useCallback,
  useState,
} from "react";

import api from "../services/api";

import {
  useSpeechRecognition,
} from "../hooks/useSpeechRecognition";

import type {
  CitizenAnalysis,
} from "../types/citizenRequest";

interface CitizenRequestFormProps {
  onAnalysisComplete: (
    analysis: CitizenAnalysis,
    text: string,
    source: "web" | "voice"
  ) => void;
}

function CitizenRequestForm({
  onAnalysisComplete,
}: CitizenRequestFormProps) {

  const [text, setText] = useState("");

  const [inputSource, setInputSource] =
    useState<"web" | "voice">("web");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [speechLanguage, setSpeechLanguage] =
    useState("en-IN");

  const handleTranscript = useCallback(
    (transcript: string) => {
      setInputSource("voice");

      setText((currentText) => {

        if (!currentText.trim()) {
          return transcript;
        }

        return `${currentText} ${transcript}`;
      });

    },
    []
  );

  const {
    supported,
    isListening,
    error: speechError,
    startListening,
    stopListening,
  } = useSpeechRecognition(
    handleTranscript
  );

  const handleAnalyze = async () => {

    if (text.trim().length < 3) {

      setError(
        "Please describe your development issue."
      );

      return;
    }

    setLoading(true);
    setError("");

    try {

      const response =
        await api.post<CitizenAnalysis>(
          "/requests/analyze",
          {
            text: text.trim(),
          }
        );

      onAnalysisComplete(
        response.data,
        text.trim(),
        inputSource
      );

    } catch (err) {

      console.error(err);

      setError(
        "Unable to understand your request. Please try again."
      );

    } finally {

      setLoading(false);

    }
  };

  const handleVoiceStart = () => {

    setError("");

    startListening(
      speechLanguage
    );
  };

  return (
    <div className="citizen-form">

      <div className="form-header">

        <span className="eyebrow">
          CITIZEN VOICE
        </span>

        <h1>
          Tell us what your community needs.
        </h1>

        <p>
          Describe a development issue in your
          own words. You can type or speak in
          English, Bengali or Hindi.
        </p>

      </div>

      <div className="voice-controls">

        <select
          value={speechLanguage}
          onChange={(event) =>
            setSpeechLanguage(
              event.target.value
            )
          }
        >
          <option value="en-IN">
            English
          </option>

          <option value="bn-IN">
            বাংলা — Bengali
          </option>

          <option value="hi-IN">
            हिन्दी — Hindi
          </option>
        </select>

        {supported ? (

          <button
            type="button"
            className={
              isListening
                ? "voice-button listening"
                : "voice-button"
            }
            onClick={
              isListening
                ? stopListening
                : handleVoiceStart
            }
          >
            {isListening
              ? "● Stop Listening"
              : "🎙 Speak"}
          </button>

        ) : (

          <span className="voice-unavailable">
            Voice input is not supported
            by this browser.
          </span>

        )}

      </div>

      <textarea
        value={text}
        onChange={(event) =>
          setText(event.target.value)
        }
        placeholder="Example: আমাদের এলাকায় পানীয় জলের সমস্যা হচ্ছে..."
        maxLength={5000}
        rows={7}
      />

      {isListening && (
        <div className="listening-indicator">
          Listening... Speak naturally.
        </div>
      )}

      {speechError && (
        <div className="error-message">
          Voice input error: {speechError}
        </div>
      )}

      <div className="form-footer">

        <span>
          {text.length}/5000
        </span>

        <button
          onClick={handleAnalyze}
          disabled={
            loading ||
            isListening
          }
        >
          {loading
            ? "Understanding..."
            : "Understand Request →"}
        </button>

      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

    </div>
  );
}

export default CitizenRequestForm;