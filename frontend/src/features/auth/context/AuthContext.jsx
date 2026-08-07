import { createContext, useContext, useEffect, useState } from 'react';

import api from '../../../services/api';
import { extractErrorMessage } from '../../../utils/errors';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadCurrentUser = async () => {
    const token = localStorage.getItem('access_token');

    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    try {
      const response = await api.get('/auth/me');
      setUser(response.data);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadCurrentUser();
  }, []);

  const login = async (username, password, rememberMe) => {
    const response = await api.post('/auth/login', {
      username,
      password,
      remember_me: rememberMe,
    });

    const { access_token, refresh_token } = response.data;

    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    await loadCurrentUser();
  };

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token');

    try {
      if (refreshToken) {
        await api.post('/auth/logout', { refresh_token: refreshToken });
      }
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  const forgotPassword = async (email) => {
    try {
      return await api.post('/auth/forgot-password', { email });
    } catch (err) {
      throw new Error(extractErrorMessage(err));
    }
  };

  const hasPermission = (permissionName) => {
    return user?.permissions?.includes(permissionName) ?? false;
  };

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
    forgotPassword,
    hasPermission,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}
