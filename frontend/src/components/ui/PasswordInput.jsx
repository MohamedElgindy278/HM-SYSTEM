import { useState } from 'react';
import { Eye, EyeClosed } from 'lucide-react';

/**
 * Shared password field with a built-in show/hide toggle.
 * Replaces every hand-rolled ".input-wrapper + .toggle-password" block.
 */
export default function PasswordInput({ label, error, hint, className = '', id, ...rest }) {
  const [visible, setVisible] = useState(false);
  const inputId = id || rest.name;

  return (
    <div className="form-group">
      {label && (
        <label className="form-label" htmlFor={inputId}>
          {label}
        </label>
      )}

      <div className="password-input-wrap">
        <input
          id={inputId}
          type={visible ? 'text' : 'password'}
          className={`input password-input${error ? ' has-error' : ''} ${className}`.trim()}
          {...rest}
        />

        <button
          type="button"
          className="password-toggle-btn"
          onClick={() => setVisible((prev) => !prev)}
          aria-label={visible ? 'Hide password' : 'Show password'}
        >
          {visible ? <Eye size={18} /> : <EyeClosed size={18} />}
        </button>
      </div>

      {error ? (
        <span className="form-error">{error}</span>
      ) : hint ? (
        <span className="form-hint">{hint}</span>
      ) : null}
    </div>
  );
}
