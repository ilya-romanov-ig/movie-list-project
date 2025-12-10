import { inject } from 'vue'
import { API_KEY } from '../api/useApi'
import { useAuthStore } from '@/stores/auth'

export function useFavoriteService() {
  const api = inject(API_KEY)
  const authStore = useAuthStore()

  const getUserId = () => {
    // TODO: Получить ID пользователя из store или API
    return authStore.userId
  }

  return {
    async addFilmToFavorites(filmId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.post(`/favorites/films/${filmId}`, {}, { user_id: userId })
    },

    async removeFilmFromFavorites(filmId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.delete(`/favorites/films/${filmId}`, { user_id: userId })
    },

    async getUserFavoriteFilms() {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.get('/favorites/films', { user_id: userId })
    },

    async addActorToFavorites(actorId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.post(`/favorites/actors/${actorId}`, {}, { user_id: userId })
    },

    async removeActorFromFavorites(actorId) {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.delete(`/favorites/actors/${actorId}`, { user_id: userId })
    },

    async getUserFavoriteActors() {
      const userId = getUserId()
      if (!userId) throw new Error('User not authenticated')
      
      return api.get('/favorites/actors', { user_id: userId })
    },

    async checkFilmInFavorites(filmId) {
      try {
        const favorites = await this.getUserFavoriteFilms()
        return favorites.items.some(f => f.film_id === filmId)
      } catch (error) {
        return false
      }
    },

    async checkActorInFavorites(actorId) {
      try {
        const favorites = await this.getUserFavoriteActors()
        return favorites.items.some(a => a.actor_id === actorId)
      } catch (error) {
        return false
      }
    }
  }
}