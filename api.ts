import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 30000,
  // No default Content-Type – let each request set it (FormData needs multipart/form-data)
});

// Request interceptor – always attach token from cookie, but don't override Content-Type
api.interceptors.request.use((config) => {
  // Attach auth token from cookie
  if (typeof document !== 'undefined') {
    const match = document.cookie.match(/(?:^|;\s*)lf_token=([^;]*)/);
    if (match) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${decodeURIComponent(match[1])}`;
    }
  }
  // Only set JSON content-type if not FormData
  if (!(config.data instanceof FormData)) {
    config.headers = config.headers || {};
    config.headers['Content-Type'] = 'application/json';
  }
  return config;
});

// Response interceptor – handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        document.cookie = 'lf_token=; Max-Age=0';
        window.location.href = '/auth';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
