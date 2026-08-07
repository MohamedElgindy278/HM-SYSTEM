import { Button, Input, Card } from '../../../components/ui';
import { ArrowLeft } from 'lucide-react';

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
      <Card className="login-card" hoverable={false}>
        <div className="card-logo">📧</div>

        <h1 className="card-title">Verify OTP</h1>

        <p className="card-subtitle">Enter the 6-digit code that has been sent to your email.</p>

        <form className="login-form" onSubmit={handleVerifyOTP}>
          {errorMessage && (
            <div className="error-banner">
              <span>{errorMessage}</span>
            </div>
          )}

          <Input
            id="otp"
            name="otp"
            label="OTP Code"
            type="text"
            placeholder="123456"
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, '').slice(0, 6))}
            maxLength={6}
            required
            hint="Enter the 6-digit code sent to your email"
          />

          <Button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            disabled={isSubmitting}
            className="submit-button"
            size="lg"
          >
            {isSubmitting ? 'Verifying...' : 'Verify OTP'}
          </Button>

          <div className="otp-actions">
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

            <button
              type="button"
              className="forgot-link back-link"
              onClick={() => setAuthView('forgot-email')}
            >
              <ArrowLeft size={16} />
              Back
            </button>
          </div>
        </form>
      </Card>
    </div>
  );
}
