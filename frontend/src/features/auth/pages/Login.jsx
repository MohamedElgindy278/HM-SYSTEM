import { useEffect, useState } from 'react';
import api from '../../../services/api';

import AuthLayout from '../components/AuthLayout';
import LoginForm from '../components/LoginForm';
import ForgotPasswordForm from '../components/ForgotPasswordForm';
import ForgotOTPForm from '../components/ForgotOTPForm';
import ResetPasswordForm from '../components/ResetPasswordForm';

import { useAuth } from '../context/useAuth';
import { useNavigate } from 'react-router-dom';

const AUTH_VIEW = {
  LOGIN: 'login',
  FORGOT_EMAIL: 'forgot-email',
  FORGOT_OTP: 'forgot-otp',
  RESET: 'reset',
};

const RESEND_COOLDOWN_SECONDS = 30;

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

  const [showSuccess, setShowSuccess] = useState(false);

  const [resendCooldown, setResendCooldown] = useState(0);

  useEffect(() => {
    if (resendCooldown <= 0) return;

    const timer = setInterval(() => {
      setResendCooldown((prev) => Math.max(prev - 1, 0));
    }, 1000);

    return () => clearInterval(timer);
  }, [resendCooldown]);

  const handleSubmit = async (event) => {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await login(username, password, rememberMe);

      setShowSuccess(true);

      navigate('/dashboard', { replace: true });
    } catch (error) {
      const message = error.message || 'Something went wrong. Please try again.';

      setErrorMessage(message);

      setIsSubmitting(false);
    }
  };

  const handleForgotPassword = async (event) => {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await api.post('/auth/forgot-password', {
        email,
      });

      setResendCooldown(RESEND_COOLDOWN_SECONDS);
      setAuthView(AUTH_VIEW.FORGOT_OTP);
    } catch (error) {
      const message = error.message || 'Something went wrong. Please try again.';

      setErrorMessage(message);
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
      const message = error.message || 'Something went wrong. Please try again.';

      setErrorMessage(message);
    }
  };

  const handleVerifyOTP = async (event) => {
    event.preventDefault();

    setErrorMessage(null);
    setIsSubmitting(true);

    try {
      await api.post('/auth/verify-otp', {
        email,
        otp,
      });

      setAuthView(AUTH_VIEW.RESET);
    } catch (error) {
      const message = error.message || 'Invalid OTP.';

      setErrorMessage(message);
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
      await api.post('/auth/reset-password', {
        email,
        new_password: newPassword,
      });

      alert('Password changed successfully.');

      setUsername('');
      setPassword('');

      setEmail('');
      setOtp('');

      setNewPassword('');
      setConfirmPassword('');

      setRememberMe(false);

      setErrorMessage(null);

      setShowSuccess(false);

      setAuthView(AUTH_VIEW.LOGIN);
    } catch (error) {
      const message = error.message || 'Something went wrong.';

      setErrorMessage(message);
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
          isSubmitting={isSubmitting}
          handleSubmit={handleSubmit}
          setAuthView={setAuthView}
        />
      )}

      {authView === AUTH_VIEW.FORGOT_EMAIL && (
        <ForgotPasswordForm
          email={email}
          setEmail={setEmail}
          isSubmitting={isSubmitting}
          errorMessage={errorMessage}
          handleForgotPassword={handleForgotPassword}
          setAuthView={setAuthView}
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
          setAuthView={setAuthView}
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
          setAuthView={setAuthView}
        />
      )}
    </AuthLayout>
  );
}
