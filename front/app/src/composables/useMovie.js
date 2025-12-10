import { ref, computed } from 'vue'
import { useMovieService, useFavoriteService, useRatingService, useWatchedService } from '@/services'
import { useAuthStore } from '@/stores/auth'

export function useMovie(movieId) {
  const movie = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  const movieService = useMovieService()
  const favoriteService = useFavoriteService()
  const ratingService = useRatingService()
  const watchedService = useWatchedService()
  const authStore = useAuthStore()
  
  const isInFavorites = ref(false)
  const isWatched = ref(false)
  const userRating = ref(null)
  
  const loadMovieData = async () => {
    try {
      loading.value = true
      error.value = null
      
      // Загружаем данные фильма
      const movieData = await movieService.getFilmDetails(movieId)
      movie.value = movieData
      
      // Загружаем пользовательские данные, если авторизован
      if (authStore.isAuthenticated) {
        await Promise.all([
          loadUserFavorites(),
          loadUserWatched(),
          loadUserRating()
        ])
      }
    } catch (err) {
      error.value = err.message
      console.error('Failed to load movie:', err)
    } finally {
      loading.value = false
    }
  }
  
  const loadUserFavorites = async () => {
    try {
      isInFavorites.value = await favoriteService.checkFilmInFavorites(movieId)
    } catch (err) {
      console.error('Failed to check favorites:', err)
    }
  }
  
  const loadUserWatched = async () => {
    try {
      isWatched.value = await watchedService.checkIfWatched(movieId)
    } catch (err) {
      console.error('Failed to check watched:', err)
    }
  }
  
  const loadUserRating = async () => {
    try {
      userRating.value = await ratingService.getUserRating(movieId)
    } catch (err) {
      console.error('Failed to load user rating:', err)
    }
  }
  
  const toggleFavorite = async () => {
    if (!authStore.isAuthenticated) {
      // TODO: Редирект на логин
      return
    }
    
    try {
      if (isInFavorites.value) {
        await favoriteService.removeFilmFromFavorites(movieId)
      } else {
        await favoriteService.addFilmToFavorites(movieId)
      }
      isInFavorites.value = !isInFavorites.value
    } catch (err) {
      console.error('Failed to toggle favorite:', err)
    }
  }
  
  const toggleWatched = async () => {
    if (!authStore.isAuthenticated) {
      // TODO: Редирект на логин
      return
    }
    
    try {
      if (isWatched.value) {
        await watchedService.unmarkAsWatched(movieId)
      } else {
        await watchedService.markAsWatched(movieId)
      }
      isWatched.value = !isWatched.value
    } catch (err) {
      console.error('Failed to toggle watched:', err)
    }
  }
  
  const rateMovie = async (rating) => {
    if (!authStore.isAuthenticated) {
      // TODO: Редирект на логин
      return
    }
    
    try {
      await ratingService.rateFilm(movieId, rating)
      userRating.value = rating
    } catch (err) {
      console.error('Failed to rate movie:', err)
    }
  }
  
  const removeRating = async () => {
    if (!authStore.isAuthenticated) {
      return
    }
    
    try {
      await ratingService.removeRating(movieId)
      userRating.value = null
    } catch (err) {
      console.error('Failed to remove rating:', err)
    }
  }
  
  return {
    movie,
    loading,
    error,
    isInFavorites,
    isWatched,
    userRating,
    loadMovieData,
    toggleFavorite,
    toggleWatched,
    rateMovie,
    removeRating,
  }
}
