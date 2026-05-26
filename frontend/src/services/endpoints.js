import api from './api'

export const authAPI = {
  signup: (email, name, password) =>
    api.post('/auth/signup', { email, name, password, role: 'student' }),

  login: (email, password) =>
    api.post('/auth/login', { email, password }),

  logout: () =>
    api.post('/auth/logout'),

  refreshToken: (refreshToken) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
}

export const examsAPI = {
  getExams: (params) =>
    api.get('/exams', { params }),

  getExamById: (examId) =>
    api.get(`/exams/${examId}`),

  createExam: (examData) =>
    api.post('/exams', examData),

  updateExam: (examId, examData) =>
    api.put(`/exams/${examId}`, examData),
}

export const questionsAPI = {
  getQuestions: (examId, params) =>
    api.get(`/questions/exam/${examId}`, { params }),

  addQuestion: (questionData) =>
    api.post('/questions', questionData),
}

export const resultsAPI = {
  submitTest: (resultData) =>
    api.post('/results/submit', resultData),

  getResult: (resultId) =>
    api.get(`/results/${resultId}`),

  getUserResults: (params) =>
    api.get('/results/user', { params }),
}

export const aiAPI = {
  doubtSolver: (formData) =>
    api.post('/ai/doubt-solver', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  getRecommendations: () =>
    api.get('/ai/recommendations'),
}

export const analyticsAPI = {
  getDashboard: () =>
    api.get('/analytics/dashboard'),

  getLeaderboard: (params) =>
    api.get('/analytics/leaderboard', { params }),
}
