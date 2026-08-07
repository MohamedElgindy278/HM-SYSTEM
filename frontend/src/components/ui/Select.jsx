/**
 * Shared dropdown select. `options` is [{ value, label }, ...].
 */
export default function Select({
  label,
  error,
  hint,
  options = [],
  placeholder,
  className = '',
  id,
  ...rest
}) {
  const selectId = id || rest.name;

  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={selectId}>
          {label}
        </label>
      )}

      <select
        id={selectId}
        className={`select${error ? ' has-error' : ''} ${className}`.trim()}
        {...rest}
      >
        {placeholder && <option value="">{placeholder}</option>}
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>

      {error ? (
        <span className="form-error">{error}</span>
      ) : hint ? (
        <span className="form-hint">{hint}</span>
      ) : null}
    </div>
  );
}
