export default function ForgotOTPForm({
  otp,
  setOtp,

  isSubmitting,

  errorMessage,

  handleVerifyOTP,
  handleResendOtp,
  resendCooldown,

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

        <h1 className="card-title">Verify OTP</h1>

        <p className="card-subtitle">Enter the 6-digit code that has been sent to your email.</p>

        <form className="login-form" onSubmit={handleVerifyOTP}>
          {errorMessage && (
            <div className="error-banner">
              <span>{errorMessage}</span>
            </div>
          )}

          <div className="form-field">
            <label className="form-label" htmlFor="otp">
              OTP Code
            </label>

            <div className="input-wrapper">
              <input
                id="otp"
                type="text"
                className="form-input"
                placeholder="123456"
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
                maxLength={6}
                required
              />
            </div>
          </div>

          <button type="submit" className="submit-button" disabled={isSubmitting}>
            <span>{isSubmitting ? 'Verifying...' : 'Verify OTP'}</span>
          </button>

          <button
            type="button"
            className="forgot-link"
            onClick={handleResendOtp}
            disabled={resendCooldown > 0}
          >
            {resendCooldown > 0
              ? `Resend OTP in ${resendCooldown}s`
              : "Didn't get a code? Resend OTP"}
          </button>

          <button type="button" className="forgot-link" onClick={() => setAuthView('forgot-email')}>
            ← Back
          </button>
        </form>
      </div>
    </div>
  );
}
