import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useGenreService() {
  const api = inject(API_KEY)

  return {
    async getGenres(params = {}) {
      return api.get('/genres', params)
    },

    async getGenreDetails(genreId) {
      return api.get(`/genres/${genreId}`)
    },

    async getGenreFilms(genreId) {
      return api.get(`/genres/${genreId}/films`)
    }
  }
}