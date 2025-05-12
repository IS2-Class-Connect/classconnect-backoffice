import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:3000',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    config.headers['Authorization'] = `Bearer admin-token`;
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
