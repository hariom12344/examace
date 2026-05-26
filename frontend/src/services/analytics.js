import api from './api';

const analyticsAPI = {
  // Get dashboard statistics
  getDashboardStats: async () => {
    const response = await api.get('/analytics/dashboard');
    return response.data;
  },

  // Get performance by topic
  getPerformanceByTopic: async () => {
    const response = await api.get('/analytics/performance-by-topic');
    return response.data;
  },

  // Get weak areas
  getWeakAreas: async (threshold = 60) => {
    const response = await api.get(`/analytics/weak-areas?threshold=${threshold}`);
    return response.data;
  },

  // Get strong areas
  getStrongAreas: async (threshold = 75) => {
    const response = await api.get(`/analytics/strong-areas?threshold=${threshold}`);
    return response.data;
  },

  // Get score trend
  getScoreTrend: async (days = 30) => {
    const response = await api.get(`/analytics/score-trend?days=${days}`);
    return response.data;
  },

  // Get accuracy vs speed analysis
  getAccuracyVsSpeed: async () => {
    const response = await api.get('/analytics/accuracy-vs-speed');
    return response.data;
  },

  // Get personalized recommendations
  getRecommendations: async () => {
    const response = await api.get('/analytics/recommendations');
    return response.data;
  },

  // Get performance by exam type
  getExamTypePerformance: async () => {
    const response = await api.get('/analytics/exam-type-performance');
    return response.data;
  },

  // Get study suggestions
  getStudySuggestions: async () => {
    const response = await api.get('/analytics/study-suggestions');
    return response.data;
  }
};

export default analyticsAPI;
