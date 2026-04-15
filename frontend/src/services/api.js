import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  register: async (username, email, password, role) => {
    const response = await api.post('/api/auth/register', {
      username,
      email,
      password,
      role,
    });
    return response.data;
  },

  login: async (username, password) => {
    const response = await api.post('/api/auth/login', {
      username,
      password,
    });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

export const patientService = {
  createProfile: async (patientData) => {
    const response = await api.post('/api/patients/', patientData);
    return response.data;
  },

  getMyProfile: async () => {
    const response = await api.get('/api/patients/me');
    return response.data;
  },

  getProfile: async (patientId) => {
    const response = await api.get(`/api/patients/${patientId}`);
    return response.data;
  },

  updateProfile: async (patientId, patientData) => {
    const response = await api.put(`/api/patients/${patientId}`, patientData);
    return response.data;
  },
};

export const healthDataService = {
  logHealthData: async (healthData) => {
    const response = await api.post('/api/health-data/', healthData);
    return response.data;
  },

  getRecords: async (patientId, days = 30) => {
    const response = await api.get(`/api/health-data/me?days=${days}`);
    return response.data;
  },

  getLatest: async (patientId) => {
    const response = await api.get(`/api/health-data/me/latest`);
    return response.data;
  },

  getTrends: async (patientId, days = 30) => {
    const response = await api.get(`/api/health-data/me/trends?days=${days}`);
    return response.data;
  },
};

export const alertService = {
  getAlerts: async (patientId) => {
    const response = await api.get(`/api/alerts/me`);
    return response.data;
  },

  getUnresolved: async (patientId) => {
    const response = await api.get(`/api/alerts/me/unresolved`);
    return response.data;
  },

  resolveAlert: async (alertId) => {
    const response = await api.put(`/api/alerts/${alertId}/resolve`);
    return response.data;
  },
};

export const recommendationService = {
  generateRecommendations: async (patientId) => {
    const response = await api.get(`/api/recommendations/me/generate`);
    return response.data;
  },

  getRecommendations: async (patientId) => {
    const response = await api.get(`/api/recommendations/me`);
    return response.data;
  },

  getInsights: async (patientId) => {
    const response = await api.get(`/api/recommendations/me/insights`);
    return response.data;
  },
};

export const doctorService = {
  getDoctors: async (skip = 0, limit = 100) => {
    const response = await api.get(`/api/doctors/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getDoctor: async (doctorId) => {
    const response = await api.get(`/api/doctors/${doctorId}`);
    return response.data;
  },

  getDoctorsBySpecialty: async (specialty) => {
    const response = await api.get(`/api/doctors/specialization/${specialty}`);
    return response.data;
  },
};

export const chatService = {
  sendMessage: async (message) => {
    const response = await api.post('/api/chat/healthcare-consultant', {
      message,
    });
    return response.data;
  },
};

export default api;
