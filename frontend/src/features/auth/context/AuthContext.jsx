import { useCallback, useEffect, useMemo, useState } from 'react';

import api from '../../../services/api';

import { AuthContext } from './AuthContext';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadCurrentUser = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    let isMounted = true;

    const initializeAuth = async () => {
      await loadCurrentUser();

      if (!isMounted) {
        return;
      }
    };

    void initializeAuth();

    return () => {
      isMounted = false;
    };
  }, [loadCurrentUser]);

  const login = useCallback(
    async (username, password, rememberMe) => {
      const response = await api.post('/auth/login', {
        username,
        password,
        remember_me: rememberMe,
      });

      const { access_token, refresh_token } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      await loadCurrentUser();
    },
    [loadCurrentUser]
  );

  const logout = useCallback(async () => {
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
  }, []);

  const forgotPassword = useCallback(async (email) => {
    return api.post('/auth/forgot-password', { email });
  }, []);

  const hasPermission = useCallback(
    (permissionName) => user?.permissions?.includes(permissionName) ?? false,
    [user]
  );

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: !!user,
      isLoading,
      login,
      logout,
      forgotPassword,
      hasPermission,
    }),
    [user, isLoading, login, logout, forgotPassword, hasPermission]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
