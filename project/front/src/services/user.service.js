import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useUserService() {
  const api = inject(API_KEY)

  return {
    async getUser(userId) {
      return api.get(`/users/${userId}`)
    },

    async searchUsers(query, params = {}) {
      return api.get('/users', { q: query, ...params })
    },

    async updateUser(userId, data) {
      return api.put(`/users/${userId}`, data)
    }
  }
}