import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useAuthService() {
  const api = inject(API_KEY)

  return {
    async register(username, email, password) {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('email', email)
      formData.append('password', password)
      
      return api.post('/auth/register', formData)
    },

    async login(email, password) {
      const formData = new FormData()
      formData.append('username', email) // В API указано username=email
      formData.append('password', password)
      
      return api.post('/auth/login', formData)
    },

    async getCurrentUser() {
      return api.get('/auth/me')
    },

    async logout() {
      // На бэкенде обычно токен инвалидируется на клиенте
      localStorage.removeItem('token')
    }
  }
}