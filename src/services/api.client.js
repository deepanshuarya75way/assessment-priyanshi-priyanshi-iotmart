import axios from 'axios';

// Get backend URL from environment variable, or fallback dynamically
export const API_URL = import.meta.env.VITE_API_URL || (
  typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
    ? `${window.location.protocol}//${window.location.hostname}:8000/api`
    : 'http://localhost:8000/api'
);

// Base Host for static images/uploads (without trailing /api)
export const BASE_HOST = API_URL.replace(/\/api\/?.*$/, '');

// WebSocket URL for live telemetry
export const WS_BASE_URL = API_URL.replace(/^http/, 'ws').replace(/\/api\/?.*$/, '');

const apiClient = axios.create({
  baseURL: API_URL,
});

// Auth Interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
