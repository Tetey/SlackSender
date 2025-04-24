import axios from 'axios';
import { ScheduledMessage } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // Include credentials in cross-origin requests
});

// Add request interceptor to handle CORS preflight
api.interceptors.request.use(
  (config) => {
    // Ensure the Origin header is set properly
    if (!config.headers['Origin']) {
      config.headers['Origin'] = window.location.origin;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const messageService = {
  getMessages: async (): Promise<ScheduledMessage[]> => {
    const response = await api.get('/messages/');
    return response.data;
  },
  
  getMessage: async (id: number): Promise<ScheduledMessage> => {
    const response = await api.get(`/messages/${id}/`);
    return response.data;
  },
  
  createMessage: async (message: ScheduledMessage): Promise<ScheduledMessage> => {
    const response = await api.post('/messages/', message);
    return response.data;
  },
  
  updateMessage: async (id: number, message: ScheduledMessage): Promise<ScheduledMessage> => {
    const response = await api.put(`/messages/${id}/`, message);
    return response.data;
  },
  
  deleteMessage: async (id: number): Promise<void> => {
    await api.delete(`/messages/${id}/`);
  },
  
  sendMessage: async (id: number): Promise<any> => {
    const response = await api.post('/messages/send_message/', { id });
    return response.data;
  }
};

export default api;
