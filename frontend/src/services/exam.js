import api from './api';

const examAPI = {
  // Get all exams with filters
  getExams: async (examType = null, difficulty = null, isPyq = null, skip = 0, limit = 10) => {
    const params = new URLSearchParams();
    if (examType) params.append('exam_type', examType);
    if (difficulty) params.append('difficulty', difficulty);
    if (isPyq !== null) params.append('is_pyq', isPyq);
    params.append('skip', skip);
    params.append('limit', limit);
    
    const response = await api.get(`/exams?${params.toString()}`);
    return response.data;
  },

  // Get single exam details
  getExam: async (examId) => {
    const response = await api.get(`/exams/${examId}`);
    return response.data;
  },

  // Create new exam (admin/instructor only)
  createExam: async (examData) => {
    const response = await api.post('/exams', examData);
    return response.data;
  },

  // Update exam
  updateExam: async (examId, examData) => {
    const response = await api.put(`/exams/${examId}`, examData);
    return response.data;
  },

  // Delete exam
  deleteExam: async (examId) => {
    const response = await api.delete(`/exams/${examId}`);
    return response.data;
  },

  // Get exam statistics
  getExamStats: async (examId) => {
    const response = await api.get(`/exams/${examId}/stats`);
    return response.data;
  },

  // Get questions for an exam (without answers)
  getExamQuestions: async (examId) => {
    const response = await api.get(`/questions/exam/${examId}`);
    return response.data;
  },

  // Get leaderboard for an exam
  getExamLeaderboard: async (examId, limit = 10) => {
    const response = await api.get(`/results/exam/${examId}/leaderboard?limit=${limit}`);
    return response.data;
  },

  // Submit test results
  submitTest: async (examId, answers, totalTime) => {
    const response = await api.post('/results', {
      exam_id: examId,
      answers: answers,
      total_time: totalTime
    });
    return response.data;
  },

  // Get result details
  getResult: async (resultId) => {
    const response = await api.get(`/results/${resultId}`);
    return response.data;
  },

  // Get user's result for an exam
  getMyExamResult: async (examId) => {
    try {
      const response = await api.get(`/results/exam/${examId}/my-result`);
      return response.data;
    } catch (error) {
      if (error.response?.status === 404) {
        return null; // No result yet
      }
      throw error;
    }
  },

  // Get user's result history
  getResultHistory: async (skip = 0, limit = 10) => {
    const response = await api.get(`/results/user/history?skip=${skip}&limit=${limit}`);
    return response.data;
  }
};

export default examAPI;
