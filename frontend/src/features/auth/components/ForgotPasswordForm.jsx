export default function ForgotPasswordForm({
  email,
  setEmail,

  isSubmitting,

  errorMessage,

  handleForgotPassword,

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

        <h1 className="card-title">Forgot Password</h1>

        <p className="card-subtitle">
          Enter your registered email address. We'll send a One-Time Password (OTP) to verify your
          identity.
        </p>

        <form className="login-form" onSubmit={handleForgotPassword}>
          {errorMessage && (
            <div className="error-banner">
              <span>{errorMessage}</span>
            </div>
          )}

          <div className="form-field">
            <label className="form-label" htmlFor="email">
              Email Address
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
                <path d="M4 6h16v12H4z" />
                <path d="M4 7l8 6 8-6" />
              </svg>

              <input
                id="email"
                type="email"
                className="form-input"
                placeholder="example@gmail.com"
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-button" disabled={isSubmitting}>
            <span>{isSubmitting ? 'Sending OTP...' : 'Send OTP'}</span>
          </button>

          <button type="button" className="forgot-link" onClick={() => setAuthView('login')}>
            ← Back to Login
          </button>
        </form>
      </div>
    </div>
  );
}
