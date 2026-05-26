import api from './api'

export const authAPI = {
  signup: (email, name, password) =>
    api.post('/auth/signup', { email, name, password }),

  login: (email, password) =>
    api.post('/auth/login', { email, password }),

  logout: () => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    return api.post('/auth/logout')
  },

  refreshToken: (refreshToken) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),

  getCurrentUser: () =>
    api.get('/auth/me'),
}

export const setAuthTokens = (data) => {
  localStorage.setItem('accessToken', data.access_token)
  localStorage.setItem('refreshToken', data.refresh_token)
  localStorage.setItem('user', JSON.stringify({
    id: data.id,
    email: data.email,
    name: data.name,
    role: data.role,
  }))
}

export const getAuthTokens = () => ({
  accessToken: localStorage.getItem('accessToken'),
  refreshToken: localStorage.getItem('refreshToken'),
})

export const getStoredUser = () => {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user) : null
}

export const clearAuth = () => {
  localStorage.removeItem('accessToken')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('user')
}
