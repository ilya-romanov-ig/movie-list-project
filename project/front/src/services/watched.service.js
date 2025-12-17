import { inject } from 'vue'
import { API_KEY } from '../api/useApi'
import { useAuthStore } from '@/stores/auth'

export function useWatchedService() {
  const api = inject(API_KEY)
  const authStore = useAuthStore()

  const getUserId = () => {
    // TODO: Получить ID пользователя из store или API
    return authStore.userId
  }

  return {
    async markAsWatched(filmId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.post(`/watched/${filmId}`, {}, { user_id: userId })
    },

    async unmarkAsWatched(filmId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.delete(`/watched/${filmId}`, { user_id: userId })
    },

    async getWatchedFilms() {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.get('/watched', { user_id: userId })
    },

    async checkIfWatched(filmId) {
      try {
        const watched = await this.getWatchedFilms()
        return watched.film_ids.includes(filmId)
      } catch (error) {
        return false
      }
    }
  }
}