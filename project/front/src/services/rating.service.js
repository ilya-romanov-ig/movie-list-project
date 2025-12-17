import { inject } from 'vue'
import { API_KEY } from '../api/useApi'
import { useAuthStore } from '@/stores/auth'

export function useRatingService() {
  const api = inject(API_KEY)
  const authStore = useAuthStore()

  const getUserId = () => {
    // TODO: Получить ID пользователя из store или API
    return authStore.userId
  }

  return {
    async rateFilm(filmId, rating) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.post(`/ratings/${filmId}`, {}, { 
        rating: rating,
        user_id: userId 
      })
    },

    async removeRating(filmId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.delete(`/ratings/${filmId}`, { user_id: userId })
    },

    async getFilmRatings(filmId) {
      return api.get(`/ratings/${filmId}`)
    },

    async getAverageRating(filmId) {
      return api.get(`/ratings/${filmId}/avg`)
    },

    async getUserRating(filmId) {
      const userId = getUserId()
      if (!userId) return null
      
      try {
        const ratings = await this.getFilmRatings(filmId)
        const userRating = ratings.items.find(r => r.user_id === userId)
        return userRating ? userRating.rating : null
      } catch (error) {
        return null
      }
    }
  }
}