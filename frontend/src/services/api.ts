import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  sendMessage: async (message: string) => {
    const response = await api.post('/api/chat/message', { message });
    return response.data;
  },

  getConversations: async () => {
    const response = await api.get('/api/chat/conversations');
    return response.data;
  },

  getConversation: async (id: string) => {
    const response = await api.get(`/api/chat/conversations/${id}`);
    return response.data;
  },

  deleteConversation: async (id: string) => {
    const response = await api.delete(`/api/chat/conversations/${id}`);
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default api;