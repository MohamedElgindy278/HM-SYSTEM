export default function Textarea({ label, error, hint, className = '', id, ...rest }) {
  const textareaId = id || rest.name;

  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={textareaId}>
          {label}
        </label>
      )}

      <textarea
        id={textareaId}
        className={`textarea${error ? ' has-error' : ''} ${className}`.trim()}
        {...rest}
      />

      {error ? (
        <span className="form-error">{error}</span>
      ) : hint ? (
        <span className="form-hint">{hint}</span>
      ) : null}
    </div>
  );
}
