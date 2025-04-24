import axios from 'axios';
import { ScheduledMessage } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Remove the proxy configuration as it's not needed and can cause issues
const baseURL = `${API_URL}/api`;

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: false,  // Keep this false to avoid preflight issues
});

// Remove the request interceptor that was incorrectly adding CORS headers
// CORS headers must only be set by the server, not the client

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
    const response = await api.post(`/messages/${id}/send/`, {});
    return response.data;
  }
};

export default api;
