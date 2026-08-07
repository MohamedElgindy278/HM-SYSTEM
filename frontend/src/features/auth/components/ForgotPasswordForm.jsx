import { Button, Input, Card } from '../../../components/ui';
import { ArrowLeft, Mail } from 'lucide-react';

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
      <Card className="login-card" hoverable={false}>
        <div className="card-logo">🔐</div>

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

          <Input
            id="email"
            name="email"
            label="Email Address"
            type="email"
            placeholder="example@gmail.com"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            icon={Mail}
          />

          <Button
            type="submit"
            variant="primary"
            loading={isSubmitting}
            disabled={isSubmitting}
            className="submit-button"
            size="lg"
          >
            {isSubmitting ? 'Sending OTP...' : 'Send OTP'}
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
