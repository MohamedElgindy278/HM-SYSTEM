import { Eye, EyeClosed } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function LoginForm({
  username,
  setUsername,

  password,
  setPassword,

  rememberMe,
  setRememberMe,

  showPassword,
  setShowPassword,

  errorMessage,
  showSuccess,

  isSubmitting,

  handleSubmit,

  setAuthView,
}) {
  return (
    <div className="form-panel">
      <div className="login-card">
        <div className="card-logo">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{
              width: 28,
              height: 28,
              color: '#fff',
            }}
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 1 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z" />
          </svg>
        </div>

        <h1 className="card-title">Welcome back</h1>
        <p className="card-subtitle">Sign in to your MedCore HMS workspace</p>

        <form className="login-form" onSubmit={handleSubmit}>
          {errorMessage && (
            <div className="error-banner">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                style={{ width: 17, height: 17, stroke: '#EF4444', flexShrink: 0, marginTop: 1 }}
              >
                <circle cx="12" cy="12" r="9" />
                <path d="M12 8v5M12 16h.01" />
              </svg>
              <span>{errorMessage}</span>
            </div>
          )}

          {showSuccess && (
            <div className="success-banner">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                style={{ width: 17, height: 17, stroke: '#22C55E', flexShrink: 0, marginTop: 1 }}
              >
                <circle cx="12" cy="12" r="9" />
                <path d="M8 12.5l2.5 2.5L16 9" />
              </svg>
              <span>Signed in successfully. Redirecting to your dashboard…</span>
            </div>
          )}

          <div className="form-field">
            <label className="form-label" htmlFor="username">
              Staff ID / Username
            </label>
            <div className="input-wrapper">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="input-icon"
              >
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
              <input
                type="text"
                id="username"
                name="username"
                placeholder="e.g. DR-4021 or receptionist01"
                autoComplete="username"
                className="form-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-field">
            <label className="form-label" htmlFor="password">
              Password
            </label>
            <div className="input-wrapper">
              <svg
                viewBox="0 0 24 24"
                fill="none"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="input-icon"
              >
                <rect x="4" y="10" width="16" height="10" rx="2" />
                <path d="M8 10V7a4 4 0 0 1 8 0v3" />
              </svg>
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                placeholder="Enter your password"
                autoComplete="current-password"
                className="form-input password-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button
                type="button"
                className="toggle-password"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                onClick={() => {
                  setShowPassword((prev) => !prev);
                }}
              >
                {showPassword ? <Eye size={18} /> : <EyeClosed size={18} />}
              </button>
            </div>
          </div>

          <div className="form-options">
            <input
              id="rememberMe"
              className="remember-input"
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            />

            <label htmlFor="rememberMe" className="remember-checkbox">
              <span className="checkbox-custom">
                {rememberMe && (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{
                      width: 12,
                      height: 12,
                      stroke: '#fff',
                    }}
                  >
                    <path d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </span>

              <span className="remember-label">Remember me</span>
            </label>
            <button
              type="button"
              className="forgot-link"
              onClick={() => setAuthView('forgot-email')}
            >
              Forgot password?
            </button>
          </div>

          <button type="submit" className="submit-button" disabled={isSubmitting}>
            <span>{isSubmitting ? 'Signing in…' : 'Sign In to Dashboard'}</span>
          </button>

          <p className="login-note">
            Secure staff access only. Contact your administrator if you don't have login
            credentials.
          </p>
        </form>

        <div className="card-footer">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ width: 14, height: 14, stroke: '#94A3B8' }}
          >
            <rect x="4" y="10" width="16" height="10" rx="2" />
            <path d="M8 10V7a4 4 0 0 1 8 0v3" />
          </svg>
          Secure Enterprise Access · Session encrypted end-to-end
        </div>
      </div>
    </div>
  );
}
