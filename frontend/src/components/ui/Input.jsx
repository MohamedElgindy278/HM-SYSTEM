/**
 * Shared text input with built-in label/hint/error slots, used across
 * every form in the app (Login, Add Patient, Add Doctor...).
 *
 * @param {import('react').ElementType} [icon] - optional leading icon
 *   (e.g. Search in the Navbar's search box)
 */
export default function Input({ label, error, hint, icon: Icon, className = '', id, ...rest }) {
  const inputId = id || rest.name;

  const input = (
    <input
      id={inputId}
      className={`input${error ? ' has-error' : ''}${Icon ? ' input-with-icon' : ''} ${className}`.trim()}
      {...rest}
    />
  );

  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={inputId}>
          {label}
        </label>
      )}

      {Icon ? (
        <div className="input-icon-wrap">
          <Icon size={16} className="input-icon" />
          {input}
        </div>
      ) : (
        input
      )}

      {error ? (
        <span className="form-error">{error}</span>
      ) : hint ? (
        <span className="form-hint">{hint}</span>
      ) : null}
    </div>
  );
}
