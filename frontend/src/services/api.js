import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,

  headers: {
    'Content-Type': 'application/json',
  },
});

// ======================================
// Request Interceptor
// ======================================

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access_token');

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },

  (error) => {
    return Promise.reject(error);
  }
);

// ======================================
// Response Interceptor
// ======================================

const AUTH_ENDPOINTS_EXEMPT_FROM_REFRESH = ['/auth/login', '/auth/refresh'];

function isExemptFromRefresh(url) {
  return AUTH_ENDPOINTS_EXEMPT_FROM_REFRESH.some((path) => url?.includes(path));
}

let isRefreshing = false;
let pendingRequests = [];

function resolvePendingRequests(newAccessToken) {
  pendingRequests.forEach((resolve) => resolve(newAccessToken));
  pendingRequests = [];
}

function rejectPendingRequests(error) {
  pendingRequests.forEach((resolve) => resolve(Promise.reject(error)));
  pendingRequests = [];
}

function forceLogout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/';
}

api.interceptors.response.use(
  (response) => {
    return response.data;
  },

  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status !== 401 || isExemptFromRefresh(originalRequest.url)) {
      return Promise.reject(error);
    }

    if (originalRequest._retry) {
      forceLogout();
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    if (isRefreshing) {
      return new Promise((resolve) => {
        pendingRequests.push(resolve);
      }).then((newAccessToken) => {
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);
      });
    }

    isRefreshing = true;

    try {
      const refreshToken = localStorage.getItem('refresh_token');

      if (!refreshToken) {
        throw new Error('Refresh token not found.');
      }

      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/auth/refresh`,

        {
          refresh_token: refreshToken,
        }
      );

      const {
        access_token,

        refresh_token,
      } = response.data;

      localStorage.setItem('access_token', access_token);
      localStorage.setItem('refresh_token', refresh_token);

      resolvePendingRequests(access_token);

      originalRequest.headers.Authorization = `Bearer ${access_token}`;

      return api(originalRequest);
    } catch (refreshError) {
      rejectPendingRequests(refreshError);
      forceLogout();
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
