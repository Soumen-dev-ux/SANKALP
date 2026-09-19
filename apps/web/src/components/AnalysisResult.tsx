import type { CitizenAnalysis } from "../types/citizenRequest";

interface AnalysisResultProps {
  analysis: CitizenAnalysis;
  originalText: string;

  onConfirm: () => void;
  onEdit: () => void;
}

function AnalysisResult({
  analysis,
  originalText,
  onConfirm,
  onEdit,
}: AnalysisResultProps) {
  const languageNames: Record<string, string> = {
    en: "English",
    bn: "Bengali",
    hi: "Hindi",
  };

  const language =
    analysis.language
      ? languageNames[analysis.language] ||
        analysis.language
      : "Unknown";

  return (
    <div className="analysis-card">

      <div className="analysis-header">
        <span className="eyebrow">
          AI UNDERSTANDING
        </span>

        <h2>
          We understood your request as:
        </h2>

        <p className="original-request">
          “{originalText}”
        </p>
      </div>

      <div className="analysis-grid">

        <div className="analysis-item">
          <span>Language</span>
          <strong>{language}</strong>
        </div>

        <div className="analysis-item">
          <span>Category</span>
          <strong>
            {analysis.category || "Not identified"}
          </strong>
        </div>

        <div className="analysis-item">
          <span>Issue</span>
          <strong>
            {analysis.issue || "Not identified"}
          </strong>
        </div>

        <div className="analysis-item">
          <span>Intent</span>
          <strong>
            {analysis.intent || "Not identified"}
          </strong>
        </div>

        <div className="analysis-item">
          <span>Location</span>
          <strong>
            {analysis.location_text ||
              "Not identified yet"}
          </strong>
        </div>

      </div>

      <div className="analysis-note">
        Please review this information before
        submitting your request.
      </div>

      <div className="analysis-actions">

        <button
          className="secondary-button"
          onClick={onEdit}
        >
          ← Edit Request
        </button>

        <button
          className="primary-button"
          onClick={onConfirm}
        >
          Confirm & Submit →
        </button>

      </div>

    </div>
  );
}

export default AnalysisResult;