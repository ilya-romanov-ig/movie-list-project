import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useAuthService() {
  const api = inject(API_KEY)

  return {
    async register(username, email, password) {
  // Отправляем как JSON объект
    return api.post('/auth/register', {
      username,
      email, 
      password
    })
  },

    async login(email, password) {
      
      return api.post('/auth/login',  {
        email, 
        password
    })
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