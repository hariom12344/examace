// API Configuration
import axios from 'axios'

// Use relative path for development, full URL for production
const API_BASE_URL = import.meta.env.DEV ? '/api' : (import.meta.env.VITE_API_URL || 'http://localhost:8000') + '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  console.log('[API DEBUG] Request URL:', config.url)
  console.log('[API DEBUG] Token from storage (first 50 chars):', token ? token.substring(0, 50) : 'NO TOKEN')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
    console.log('[API DEBUG] Authorization header set to Bearer token')
  } else {
    console.log('[API DEBUG] WARNING: No token found in localStorage')
  }
  return config
})

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('accessToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
