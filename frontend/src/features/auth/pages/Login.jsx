import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import api from '../../../services/api';
import { extractErrorMessage } from '../../../utils/errors';

import AuthLayout from '../components/AuthLayout';
import LoginForm from '../components/LoginForm';
import ForgotPasswordForm from '../components/ForgotPasswordForm';
import ForgotOTPForm from '../components/ForgotOTPForm';
import ResetPasswordForm from '../components/ResetPasswordForm';

import { useAuth } from '../context/AuthContext';

const AUTH_VIEW = {
  LOGIN: 'login',
  FORGOT_EMAIL: 'forgot-email',
  FORGOT_OTP: 'forgot-otp',
  RESET: 'reset',
};

const RESEND_COOLDOWN_SECONDS = 30;
const SUCCESS_REDIRECT_DELAY_MS = 600;

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [authView, setAuthView] = useState(AUTH_VIEW.LOGIN);

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // "Signed in, redirecting..." banner shown briefly before navigating away
  const [showSuccess, setShowSuccess] = useState(false);

  // General-purpose success banner shown on the LOGIN view after a
  // password reset completes (replaces the old alert() popup)
  const [noticeMessage, setNoticeMessage] = useState(null);

  const [resendCooldown, setResendCooldown] = useState(0);

  useEffect(() => {
    if (resendCooldown <= 0) return;

    const timer = setInterval(() => {
      setResendCooldown((prev) => Math.max(prev - 1, 0));
    }, 1000);

    return () => clearInterval(timer);
  }, [resendCooldown]);

  const switchView = (view) => {
    setErrorMessage(null);
    setNoticeMessage(null);
    setAuthView(view);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await login(username, password, rememberMe);

      setShowSuccess(true);

      // Small delay so the "signed in successfully" banner is actually
      // visible for a moment before the page navigates away.
      setTimeout(() => {
        navigate('/dashboard', { replace: true });
      }, SUCCESS_REDIRECT_DELAY_MS);
    } catch (error) {
      setErrorMessage(extractErrorMessage(error));
      setIsSubmitting(false);
    }
  };

  const handleForgotPassword = async (event) => {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await api.post('/auth/forgot-password', { email });

      setResendCooldown(RESEND_COOLDOWN_SECONDS);
      setAuthView(AUTH_VIEW.FORGOT_OTP);
    } catch (error) {
      setErrorMessage(extractErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResendOtp = async () => {
    if (resendCooldown > 0) return;

    setErrorMessage(null);

    try {
      await api.post('/auth/forgot-password', { email });
      setResendCooldown(RESEND_COOLDOWN_SECONDS);
    } catch (error) {
      setErrorMessage(extractErrorMessage(error));
    }
  };

  const handleVerifyOTP = async (event) => {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await api.post('/auth/verify-otp', { email, otp });

      setAuthView(AUTH_VIEW.RESET);
    } catch (error) {
      setErrorMessage(extractErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResetPassword = async (event) => {
    event.preventDefault();

    setErrorMessage(null);

    if (newPassword !== confirmPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }

    setIsSubmitting(true);

    try {
      // NOTE: `otp` is included here so the backend can confirm this
      // reset request is tied to the OTP that was actually verified.
      // If /auth/reset-password relies purely on a short-lived session
      // set during /auth/verify-otp instead, this field is simply ignored
      // server-side - safe either way.
      await api.post('/auth/reset-password', {
        email,
        otp,
        new_password: newPassword,
      });

      setUsername('');
      setPassword('');
      setEmail('');
      setOtp('');
      setNewPassword('');
      setConfirmPassword('');
      setRememberMe(false);
      setErrorMessage(null);
      setShowSuccess(false);

      setNoticeMessage('Password changed successfully. Please sign in with your new password.');
      setAuthView(AUTH_VIEW.LOGIN);
    } catch (error) {
      setErrorMessage(extractErrorMessage(error));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout>
      {authView === AUTH_VIEW.LOGIN && (
        <LoginForm
          username={username}
          setUsername={setUsername}
          password={password}
          setPassword={setPassword}
          rememberMe={rememberMe}
          setRememberMe={setRememberMe}
          showPassword={showPassword}
          setShowPassword={setShowPassword}
          errorMessage={errorMessage}
          showSuccess={showSuccess}
          noticeMessage={noticeMessage}
          isSubmitting={isSubmitting}
          handleSubmit={handleSubmit}
          setAuthView={switchView}
        />
      )}

      {authView === AUTH_VIEW.FORGOT_EMAIL && (
        <ForgotPasswordForm
          email={email}
          setEmail={setEmail}
          isSubmitting={isSubmitting}
          errorMessage={errorMessage}
          handleForgotPassword={handleForgotPassword}
          setAuthView={switchView}
        />
      )}

      {authView === AUTH_VIEW.FORGOT_OTP && (
        <ForgotOTPForm
          otp={otp}
          setOtp={setOtp}
          isSubmitting={isSubmitting}
          errorMessage={errorMessage}
          handleVerifyOTP={handleVerifyOTP}
          handleResendOtp={handleResendOtp}
          resendCooldown={resendCooldown}
          setAuthView={switchView}
        />
      )}

      {authView === AUTH_VIEW.RESET && (
        <ResetPasswordForm
          newPassword={newPassword}
          setNewPassword={setNewPassword}
          confirmPassword={confirmPassword}
          setConfirmPassword={setConfirmPassword}
          isSubmitting={isSubmitting}
          errorMessage={errorMessage}
          handleResetPassword={handleResetPassword}
          setAuthView={switchView}
        />
      )}
    </AuthLayout>
  );
}
