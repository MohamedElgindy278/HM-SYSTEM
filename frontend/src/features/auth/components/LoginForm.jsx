import { useState } from 'react';
import { Eye, EyeClosed, Heart, User } from 'lucide-react';

import { Button, Input, Card } from '../../../components/ui';

import './Form.css';

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
  const [passwordFocused, setPasswordFocused] = useState(false);

  return (
    <div className="form-panel">
      <Card className="login-card" hoverable={false}>
        <div className="card-logo">
          <Heart size={28} color="#fff" />
        </div>

        <h1 className="card-title">Welcome back</h1>
        <p className="card-subtitle">Sign in to your MedCore HMS workspace</p>

        <form className="login-form" onSubmit={handleSubmit}>
          {/* ===== Error / Success ===== */}
          {errorMessage && (
            <div className="error-banner">
              <span>{errorMessage}</span>
            </div>
          )}

          {showSuccess && (
            <div className="success-banner">
              <span>Signed in successfully. Redirecting to your dashboard…</span>
            </div>
          )}

          {/* ===== Username ===== */}
          <Input
            id="username"
            name="username"
            label="Staff ID / Username"
            type="text"
            placeholder="e.g. DR-4021 or receptionist01"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            icon={User}
          />

          {/* ===== Password ===== */}
          <div className="form-group">
            <label className="form-label" htmlFor="password">
              Password
            </label>

            <div className="input-wrapper">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                autoComplete="current-password"
                className={`form-input password-input ${passwordFocused ? 'focused' : ''}`}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onFocus={() => setPasswordFocused(true)}
                onBlur={() => setPasswordFocused(false)}
                required
              />

              <button
                type="button"
                className="toggle-password"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                onClick={() => setShowPassword((prev) => !prev)}
              >
                {showPassword ? <Eye size={18} /> : <EyeClosed size={18} />}
              </button>
            </div>
          </div>

          {/* ===== Options ===== */}
          <div className="form-options">
            <label htmlFor="rememberMe" className="remember-checkbox">
              <input
                id="rememberMe"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="remember-input"
              />
              <span className="checkbox-custom">
                {rememberMe && (
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    style={{ width: 12, height: 12, stroke: '#fff' }}
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

          {/* ===== Submit ===== */}
          <Button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            disabled={isSubmitting}
            className="submit-button"
            size="lg"
          >
            {isSubmitting ? 'Signing in…' : 'Sign In to Dashboard'}
          </Button>

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
      </Card>
    </div>
  );
}
