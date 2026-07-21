import { useState } from 'react';
import { Eye, EyeClosed } from 'lucide-react';

export default function ResetPasswordForm({
  newPassword,
  setNewPassword,

  confirmPassword,
  setConfirmPassword,

  isSubmitting,

  errorMessage,

  handleResetPassword,

  setAuthView,
}) {
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  return (
    <div className="form-panel">
      <div className="login-card">
        <div className="card-logo">🔒</div>

        <h1 className="card-title">Reset Password</h1>

        <p className="card-subtitle">Enter your new password.</p>

        <form className="login-form" onSubmit={handleResetPassword}>
          {errorMessage && (
            <div className="error-banner">
              <span>{errorMessage}</span>
            </div>
          )}

          <div className="form-field">
            <label className="form-label" htmlFor="newPassword">
              New Password
            </label>

            <div className="input-wrapper">
              <input
                id="newPassword"
                type={showNewPassword ? 'text' : 'password'}
                className="form-input password-input"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="toggle-password"
                aria-label={showNewPassword ? 'Hide password' : 'Show password'}
                onClick={() => setShowNewPassword((prev) => !prev)}
              >
                {showNewPassword ? <Eye size={18} /> : <EyeClosed size={18} />}
              </button>
            </div>
          </div>

          <div className="form-field">
            <label className="form-label" htmlFor="confirmPassword">
              Confirm Password
            </label>

            <div className="input-wrapper">
              <input
                id="confirmPassword"
                type={showConfirmPassword ? 'text' : 'password'}
                className="form-input password-input"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="toggle-password"
                aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
                onClick={() => setShowConfirmPassword((prev) => !prev)}
              >
                {showConfirmPassword ? <Eye size={18} /> : <EyeClosed size={18} />}
              </button>
            </div>
          </div>

          <button className="submit-button" disabled={isSubmitting}>
            <span>{isSubmitting ? 'Changing...' : 'Change Password'}</span>
          </button>

          <button type="button" className="forgot-link" onClick={() => setAuthView('login')}>
            ← Back to Login
          </button>
        </form>
      </div>
    </div>
  );
}
