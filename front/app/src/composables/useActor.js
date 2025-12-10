import { ref, computed } from 'vue'
import { useActorService, useFavoriteService } from '@/services'
import { useAuthStore } from '@/stores/auth'

export function useActor(actorId) {
  const actor = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const filmography = ref([])
  const isInFavorites = ref(false)
  
  const actorService = useActorService()
  const favoriteService = useFavoriteService()
  const authStore = useAuthStore()
  
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  
  const loadActorData = async () => {
    try {
      loading.value = true
      error.value = null
      
      const [actorData, filmsData] = await Promise.all([
        actorService.getActorDetails(actorId),
        actorService.getActorFilms(actorId)
      ])
      
      actor.value = actorData
      filmography.value = filmsData.items?.slice(0, 5) || []
      
      if (isAuthenticated.value) {
        await loadUserFavorites()
      }
    } catch (err) {
      error.value = err.message
      console.error('Failed to load actor:', err)
    } finally {
      loading.value = false
    }
  }
  
  const loadUserFavorites = async () => {
    try {
      isInFavorites.value = await favoriteService.checkActorInFavorites(actorId)
    } catch (err) {
      console.error('Failed to check favorites:', err)
    }
  }
  
  const toggleFavorite = async () => {
    if (!isAuthenticated.value) {
      return false // TODO: Редирект на логин
    }
    
    try {
      if (isInFavorites.value) {
        await favoriteService.removeActorFromFavorites(actorId)
      } else {
        await favoriteService.addActorToFavorites(actorId)
      }
      isInFavorites.value = !isInFavorites.value
      return true
    } catch (err) {
      console.error('Failed to toggle favorite:', err)
      return false
    }
  }
  
  return {
    actor,
    loading,
    error,
    filmography,
    isInFavorites,
    isAuthenticated,
    loadActorData,
    toggleFavorite,
  }
}