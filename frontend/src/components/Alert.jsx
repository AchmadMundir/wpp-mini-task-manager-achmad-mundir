export default function Alert({ message, onRetry, tone = "error" }) {
  if (!message) return null;

  return (
    <div className={`alert alert-${tone}`} role="alert">
      <span>{message}</span>
      {onRetry && (
        <button className="button button-small button-ghost" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}

