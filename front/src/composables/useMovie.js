import { ref, computed } from 'vue'
import { useMovieService, useFavoriteService, useRatingService, useWatchedService } from '@/services'
import { useAuthStore } from '@/stores/auth'

export function useMovie(movieId) {
  const movie = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const imageError = ref(false) // Добавляем обработку ошибок изображения
  
  const movieService = useMovieService()
  const favoriteService = useFavoriteService()
  const ratingService = useRatingService()
  const watchedService = useWatchedService()
  const authStore = useAuthStore()
  
  const isInFavorites = ref(false)
  const isWatched = ref(false)
  const userRating = ref(null)
  
  // Вычисляемое свойство для URL постера
  const posterUrl = computed(() => {
    if (!movie.value?.poster_url) {
      return getDefaultPoster()
    }
    
    // Используем метод из movieService для формирования URL
    return movieService.formatPosterUrl(movie.value.poster_url)
  })
  
  // Функция для получения заглушки
  const getDefaultPoster = () => {
    // SVG заглушка для фильма
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgdmlld0JveD0iMCAwIDMwMCA0NTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSI0NTAiIGZpbGw9IiMxRDFFMjMiIHJ4PSI4Ii8+PHRleHQgeD0iMTUwIiB5PSIyMjAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgSGVscmV0aWNhLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4IiBmaWxsPSIjRkZGIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iNTAwIj5GaWxtIFBvc3RlcjwvdGV4dD48dGV4dCB4PSIxNTAiIHk9IjI0NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBIZWx2ZXRpY2EsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiNGRkYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtd2VpZ2h0PSIzMDAiPk5vdCBhdmFpbGFibGU8L3RleHQ+PHBhdGggZD0iTTEwMCAxNTBIMjAwTTE1MCAxMDBWMjAwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PC9zdmc+'
  }
  
  // Обработчик ошибок изображения
  const handleImageError = () => {
    console.warn('Failed to load poster for movie:', movie.value?.title)
    imageError.value = true
  }
  
  // Сброс ошибки изображения
  const resetImageError = () => {
    imageError.value = false
  }
  
  const loadMovieData = async () => {
    try {
      loading.value = true
      error.value = null
      resetImageError() // Сбрасываем ошибку изображения
      
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
      error.value = err.message || 'Не удалось загрузить данные фильма'
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
      // Можно вызвать событие для показа уведомления
      return Promise.reject(new Error('Требуется авторизация'))
    }
    
    try {
      if (isInFavorites.value) {
        await favoriteService.removeFilmFromFavorites(movieId)
      } else {
        await favoriteService.addFilmToFavorites(movieId)
      }
      isInFavorites.value = !isInFavorites.value
      return Promise.resolve()
    } catch (err) {
      console.error('Failed to toggle favorite:', err)
      return Promise.reject(err)
    }
  }
  
  const toggleWatched = async () => {
    if (!authStore.isAuthenticated) {
      return Promise.reject(new Error('Требуется авторизация'))
    }
    
    try {
      if (isWatched.value) {
        await watchedService.unmarkAsWatched(movieId)
      } else {
        await watchedService.markAsWatched(movieId)
      }
      isWatched.value = !isWatched.value
      return Promise.resolve()
    } catch (err) {
      console.error('Failed to toggle watched:', err)
      return Promise.reject(err)
    }
  }
  
  const rateMovie = async (rating) => {
    if (!authStore.isAuthenticated) {
      return Promise.reject(new Error('Требуется авторизация'))
    }
    
    if (rating < 1 || rating > 10) {
      return Promise.reject(new Error('Оценка должна быть от 1 до 10'))
    }
    
    try {
      await ratingService.rateFilm(movieId, rating)
      userRating.value = rating
      return Promise.resolve()
    } catch (err) {
      console.error('Failed to rate movie:', err)
      return Promise.reject(err)
    }
  }
  
  const removeRating = async () => {
    if (!authStore.isAuthenticated) {
      return Promise.reject(new Error('Требуется авторизация'))
    }
    
    try {
      await ratingService.removeRating(movieId)
      userRating.value = null
      return Promise.resolve()
    } catch (err) {
      console.error('Failed to remove rating:', err)
      return Promise.reject(err)
    }
  }
  
  // Функция для обновления данных фильма
  const refresh = () => {
    return loadMovieData()
  }
  
  return {
    // Данные
    movie,
    loading,
    error,
    imageError,
    
    // Состояния пользователя
    isInFavorites,
    isWatched,
    userRating,
    
    // Вычисляемые свойства
    posterUrl,
    
    // Методы
    loadMovieData,
    toggleFavorite,
    toggleWatched,
    rateMovie,
    removeRating,
    handleImageError,
    refresh
  }
}