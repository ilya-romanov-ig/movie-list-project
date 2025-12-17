import { inject } from 'vue'
import { API_KEY } from '../api/useApi'
import { useAuthStore } from '@/stores/auth'

export function useHomeService() {
  const api = inject(API_KEY)
  const authStore = useAuthStore()

  const getUserId = () => {
    return authStore.userId
  }

  return {
    async getHomeData() {
      const userId = getUserId()
      const params = userId ? { user_id: userId } : {}
      return api.get('/home', params)
    },

    async getRecommended() {
      const userId = getUserId()
      if (!userId) return { items: [] }
      
      return api.get('/home/recommended', { user_id: userId })
    },

    async getTrending() {
      return api.get('/home/trending')
    }
  }
}