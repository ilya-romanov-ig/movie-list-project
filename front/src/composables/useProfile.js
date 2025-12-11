import { ref } from 'vue'
import { useFavoriteService, useWatchedService, useUserService } from '@/services'
import { useAuthStore } from '@/stores/auth'

export function useProfile() {
  const loading = ref(false)
  const user = ref(null)
  const watchedMovies = ref([])
  const favoriteMovies = ref([])
  const favoriteActors = ref([])
  
  const favoriteService = useFavoriteService()
  const watchedService = useWatchedService()
  const userService = useUserService()
  const authStore = useAuthStore()
  
  const loadProfileData = async () => {
    try {
      loading.value = true
      
      const userId = authStore.userId
      if (!userId) {
        throw new Error('User not authenticated')
      }
      
      const [userData, favoritesData, watchedData, actorsData] = await Promise.all([
        userService.getUser(userId),
        favoriteService.getUserFavoriteFilms(),
        watchedService.getWatchedFilms(),
        favoriteService.getUserFavoriteActors()
      ])
      
      user.value = userData
      favoriteMovies.value = favoritesData.items || []
      favoriteActors.value = actorsData.items || []
      
      // TODO: Загрузить детали просмотренных фильмов
      if (watchedData.film_ids?.length > 0) {
        watchedMovies.value = watchedData.film_ids.map(id => ({
          film_id: id,
          title: `Фильм ${id}` // Временная заглушка
        }))
      }
    } catch (err) {
      console.error('Failed to load profile:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const removeFromWatched = async (movieId) => {
    try {
      await watchedService.unmarkAsWatched(movieId)
      watchedMovies.value = watchedMovies.value.filter(m => m.film_id !== movieId)
    } catch (err) {
      console.error('Failed to remove from watched:', err)
      throw err
    }
  }
  
  const removeFromFavorites = async (movieId) => {
    try {
      await favoriteService.removeFilmFromFavorites(movieId)
      favoriteMovies.value = favoriteMovies.value.filter(m => m.film_id !== movieId)
    } catch (err) {
      console.error('Failed to remove from favorites:', err)
      throw err
    }
  }
  
  const removeActorFromFavorites = async (actorId) => {
    try {
      await favoriteService.removeActorFromFavorites(actorId)
      favoriteActors.value = favoriteActors.value.filter(a => a.actor_id !== actorId)
    } catch (err) {
      console.error('Failed to remove actor from favorites:', err)
      throw err
    }
  }
  
  return {
    loading,
    user,
    watchedMovies,
    favoriteMovies,
    favoriteActors,
    loadProfileData,
    removeFromWatched,
    removeFromFavorites,
    removeActorFromFavorites,
  }
}