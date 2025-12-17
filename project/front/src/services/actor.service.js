import { inject } from 'vue'
import { API_KEY } from '../api/useApi'

export function useActorService() {
  const api = inject(API_KEY)

  return {
    async getActors(params = {}) {
      return api.get('/actors', params)
    },

    async getActorDetails(actorId) {
      return api.get(`/actors/${actorId}`)
    },

    async getActorFilms(actorId) {
      return api.get(`/actors/${actorId}/films`)
    },

    async searchActors(query, params = {}) {
      return api.get('/actors', { name: query, ...params })
    },

    async createActor(data) {
      return api.post('/actors', data)
    },

    async updateActor(actorId, data) {
      return api.patch(`/actors/${actorId}`, data)
    },

    async deleteActor(actorId) {
      return api.delete(`/actors/${actorId}`)
    }
  }
}