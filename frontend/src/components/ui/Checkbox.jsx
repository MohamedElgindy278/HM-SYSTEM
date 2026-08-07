/**
 * Shared checkbox used across the app (e.g. "Remember me", "Is Active"
 * toggles in forms, row-select in tables).
 */
export default function Checkbox({ label, checked, onChange, id, className = '', ...rest }) {
  const checkboxId = id || rest.name;

  return (
    <label htmlFor={checkboxId} className={`checkbox-wrap ${className}`.trim()}>
      <input
        id={checkboxId}
        type="checkbox"
        checked={checked}
        onChange={onChange}
        className="checkbox-input"
        {...rest}
      />
      <span className="checkbox-box" />
      {label && <span className="checkbox-label">{label}</span>}
    </label>
  );
}
