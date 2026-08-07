import { useState } from 'react';
import { Eye, EyeClosed, ArrowLeft } from 'lucide-react';

import { Button, Input, Card } from '../../../components/ui';

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
      <Card className="login-card" hoverable={false}>
        <div className="card-logo">🔒</div>

        <h1 className="card-title">Reset Password</h1>

        <p className="card-subtitle">Enter your new password.</p>

        <form className="login-form" onSubmit={handleResetPassword}>
          {errorMessage && (
            <div className="error-banner">
              <span>{errorMessage}</span>
            </div>
          )}

          <div className="form-group">
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
                minLength={8}
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
            <span className="form-hint">Must be at least 8 characters</span>
          </div>

          <div className="form-group">
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

          <Button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            disabled={isSubmitting}
            className="submit-button"
            size="lg"
          >
            {isSubmitting ? 'Changing...' : 'Change Password'}
          </Button>

          <button
            type="button"
            className="forgot-link back-link"
            onClick={() => setAuthView('login')}
          >
            <ArrowLeft size={16} />
            Back to Login
          </button>
        </form>
      </Card>
    </div>
  );
}
