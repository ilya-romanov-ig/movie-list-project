import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useSearchService() {
  const api = inject(API_KEY)

  return {
    async search(query) {
      if (!query?.trim()) {
        return { query: '', results: { films: [], actors: [], users: [] } }
      }
      
      return api.get('/search', { q: query })
    },

    async searchFilms(query, params = {}) {
      return api.get('/films', { q: query, ...params })
    },

    async searchActors(query, params = {}) {
      return api.get('/actors', { name: query, ...params })
    },

    async searchUsers(query, params = {}) {
      return api.get('/users', { q: query, ...params })
    }
  }
}