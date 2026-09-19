interface SubmissionSuccessProps {
  reference: string;
  onCreateAnother: () => void;
}

function SubmissionSuccess({
  reference,
  onCreateAnother,
}: SubmissionSuccessProps) {
  return (
    <div className="success-card">

      <div className="success-icon">
        ✓
      </div>

      <span className="eyebrow">
        REQUEST SUBMITTED
      </span>

      <h2>
        Your voice has been recorded.
      </h2>

      <p>
        Your development request has been
        successfully submitted to SANKALP.
      </p>

      <div className="reference-box">
        <span>Request Reference</span>

        <strong>
          {reference}
        </strong>
      </div>

      <p className="success-note">
        Keep this reference for future tracking.
      </p>

      <button
        className="primary-button"
        onClick={onCreateAnother}
      >
        Submit Another Request
      </button>

    </div>
  );
}

export default SubmissionSuccess;