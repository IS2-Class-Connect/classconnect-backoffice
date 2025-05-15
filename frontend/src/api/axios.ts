import axios, { AxiosInstance } from 'axios';

const api: AxiosInstance = axios.create({
  baseURL: process.env.ADMINS_URL ?? "localhost:3004",
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
