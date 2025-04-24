import axios from 'axios';
import { ScheduledMessage } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Add a proxy URL for development to bypass CORS
const useProxy = process.env.NODE_ENV === 'development' && !API_URL.includes('localhost');
const baseURL = useProxy ? `https://cors-anywhere.herokuapp.com/${API_URL}/api` : `${API_URL}/api`;

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
  withCredentials: false,  // Change to false to avoid preflight requests
});

// Add request interceptor to handle CORS preflight
api.interceptors.request.use(
  (config) => {
    // Ensure the Origin header is set properly
    if (!config.headers['Origin']) {
      config.headers['Origin'] = window.location.origin;
    }
    
    // Add CORS headers for all requests
    config.headers['Access-Control-Allow-Origin'] = '*';
    
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
