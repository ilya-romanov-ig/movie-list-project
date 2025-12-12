import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useMovieService() {
  const api = inject(API_KEY)

  return {
    async getTopFilms() {
      return api.get('/films/top')
    },

    async getNewestFilms() {
      return api.get('/films/newest')
    },

    async getFilmDetails(filmId) {
      return api.get(`/films/${filmId}/details`)
    },

    async getFilmActors(filmId) {
      return api.get(`/films/${filmId}/actors`)
    },

    async getFilmGenres(filmId) {
      return api.get(`/films/${filmId}/genres`)
    },

    async getFilmRatings(filmId) {
      return api.get(`/films/${filmId}/ratings`)
    },

    async getAverageRating(filmId) {
      return api.get(`/films/${filmId}/rating`)
    },

    async searchFilms(query, params = {}) {
      return api.get('/films', { q: query, ...params })
    },

    formatPosterUrl(filename) {
      if (!filename) return this._getDefaultPoster()
      
      const baseUrl = import.meta.env.VITE_IMAGES_URL || 
                    import.meta.env.VITE_API_URL || 
                    'http://localhost:8001'
      
      return `${baseUrl}/${filename}`
    }
  }
}