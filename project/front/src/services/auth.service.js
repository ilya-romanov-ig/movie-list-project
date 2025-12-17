import { inject } from 'vue'
import { API_KEY } from '@/api/useApi'

export function useAuthService() {
  const api = inject(API_KEY)
  
  if (!api) {
    console.error('APIClient not found in DI container')
    throw new Error('APIClient not available')
  }

  return {
    async register(username, email, password) {
      return api.post('/auth/register', { username, email, password })
    },

    async login(email, password) {
      const formData = new URLSearchParams()
      formData.append('username', email)
      formData.append('password', password)
      
      return api.request('/auth/login', {
        method: 'POST',
        body: formData.toString(),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
    },

    async getCurrentUser() {
      const token = localStorage.getItem('token')
      if (!token) {
        throw new Error('No token found')
      }
      return api.get('/auth/me')
    },

    async logout() {
      localStorage.removeItem('token')
    }
  }
}