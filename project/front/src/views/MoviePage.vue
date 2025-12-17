<template>
  <PageWrapper>
    <v-row justify="center" class="my-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          label="Поиск по фильмам и актёрам"
          clearable
          outlined
          color="white"
          prepend-inner-icon="mdi-magnify"
          class="search-field"
          @keyup.enter="performSearch"
        />
      </v-col>
    </v-row>

    <v-row v-if="loading" class="mb-8">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate size="64" />
      </v-col>
    </v-row>

    <v-row v-else-if="movieData" class="mb-8">
      <v-col cols="12" md="4" lg="3">
        <div class="poster-container">
          <v-img
            :src="posterUrl"
            aspect-ratio="2/3"
            class="movie-poster elevation-6"
            rounded
            @error="handleImageError"
            max-width="300"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height ma-0" align="center" justify="center">
                <v-progress-circular indeterminate color="grey lighten-5" />
              </v-row>
            </template>
            
            <!-- Заглушка при ошибке -->
            <template v-if="imageError" v-slot:error>
              <v-sheet
                color="grey-darken-3"
                class="d-flex align-center justify-center fill-height"
                rounded
              >
                <div class="text-center">
                  <v-icon size="64" color="grey-lighten-1">mdi-image-off</v-icon>
                  <div class="text-caption mt-2">Постер не найден</div>
                </div>
              </v-sheet>
            </template>
          </v-img>
        </div>
      </v-col>

      <v-col cols="12" md="8" lg="9">
        <div class="d-flex align-center mb-2">
          <h1 class="movie-title">{{ movieData.title }}</h1>
          <span class="movie-year ml-4">({{ movieData.release_year }})</span>
        </div>

        <div class="mb-4">
          <v-chip
            v-for="genre in movieData.genres || []"
            :key="genre.genre_id"
            class="mr-2 mb-2"
            color="primary"
            @click="goToGenre(genre)"
          >
            {{ genre.name }}
          </v-chip>
        </div>

        <div class="d-flex align-center mb-4">
          <v-icon class="mr-2">mdi-clock-outline</v-icon>
          <span class="mr-4">{{ formatDuration(movieData.runtime) }}</span>
          <v-icon class="mr-2 ml-4" color="amber">mdi-star</v-icon>
          <span class="movie-rating">{{ averageRating?.toFixed(1) || 'N/A' }}</span>
          <span class="ml-2 text-grey">({{ ratingsCount || 0 }} оценок)</span>
        </div>

        <v-row class="mb-6">
          <v-col cols="6" md="4" lg="3">
            <div class="stat-item">
              <div class="stat-value">{{ movieData.stats?.watched_count?.toLocaleString() || 0 }}</div>
              <div class="stat-label">Просмотров</div>
            </div>
          </v-col>
        </v-row>

        <div class="mb-6">
          <v-row>
            <v-col cols="12" sm="6" md="4" lg="3" v-for="action in actionButtons" :key="action.text">
              <v-btn
                :color="action.color"
                block
                :prepend-icon="action.icon"
                @click="handleAction(action.type)"
                variant="outlined"
                :loading="actionLoading[action.type]"
                :disabled="!isAuthenticated"
              >
                {{ action.text }}
              </v-btn>
            </v-col>
          </v-row>
        </div>

        <div class="mb-8">
          <h3 class="mb-2">Описание</h3>
          <p class="movie-description">{{ movieData.description || 'Описание отсутствует' }}</p>
        </div>
      </v-col>
    </v-row>

    <v-alert v-else-if="error" type="error" class="mb-8">
      {{ error }}
    </v-alert>

    <div v-if="movieData?.actors?.length > 0" class="mb-8">
      <h2 class="mb-4">Актёры</h2>
      <v-slide-group show-arrows>
        <v-slide-item v-for="actor in movieData.actors" :key="actor.id">
          <ActorCard 
            :actor="actor" 
            class="mx-3"
            @click="goToActor(actor)"
          />
        </v-slide-item>
      </v-slide-group>
    </div>

    <div v-if="similarMovies.length > 0">
      <h2 class="mb-4">Похожие фильмы</h2>
      <v-slide-group show-arrows>
        <v-slide-item v-for="similarMovie in similarMovies" :key="similarMovie.id">
          <MovieCard 
            :movie="similarMovie" 
            class="mx-3"
            @click="goToMovie(similarMovie.id)"
          />
        </v-slide-item>
      </v-slide-group>
    </div>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieCard from '@/components/MovieCard.vue'
import ActorCard from '@/components/ActorCard.vue'
import { useMovieService } from '@/services/movie.service'
import { useFavoriteService } from '@/services/favorite.service'
import { useRatingService } from '@/services/rating.service'
import { useWatchedService } from '@/services/watched.service'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const movieService = useMovieService()
const favoriteService = useFavoriteService()
const ratingService = useRatingService()
const watchedService = useWatchedService()

const searchQuery = ref('')
const loading = ref(true)
const error = ref(null)
const movieData = ref(null) // переименовали movie в movieData для ясности
const similarMovies = ref([])
const averageRating = ref(0)
const ratingsCount = ref(0)
const imageError = ref(false) // добавили обработку ошибок изображения

const isInFavorites = ref(false)
const isWatched = ref(false)
const userRating = ref(null)
const actionLoading = ref({
  favorite: false,
  watched: false,
  rate: false,
  removeRating: false
})

const isAuthenticated = computed(() => authStore.isAuthenticated)

// ВЫЧИСЛЯЕМЫЙ URL для постера
const posterUrl = computed(() => {
  if (!movieData.value?.poster_url) {
    return getDefaultPoster()
  }
  
  // Используем метод из movieService для формирования URL
  return movieService.formatPosterUrl(movieData.value.poster_url)
})

const actionButtons = computed(() => {
  const baseButtons = [
    {
      text: isInFavorites.value ? 'Удалить из избранного' : 'Добавить в избранное',
      icon: isInFavorites.value ? 'mdi-heart' : 'mdi-heart-outline',
      color: isInFavorites.value ? 'error' : 'primary',
      type: 'favorite'
    },
    {
      text: isWatched.value ? 'Удалить из просмотренного' : 'Отметить как просмотренное',
      icon: isWatched.value ? 'mdi-eye-off' : 'mdi-eye',
      color: isWatched.value ? 'grey' : 'success',
      type: 'watched'
    }
  ]

  if (userRating.value) {
    baseButtons.push(
      {
        text: 'Изменить оценку',
        icon: 'mdi-star-edit',
        color: 'amber',
        type: 'rate'
      },
      {
        text: 'Удалить оценку',
        icon: 'mdi-star-remove',
        color: 'error',
        type: 'removeRating'
      }
    )
  } else {
    baseButtons.push({
      text: 'Оценить фильм',
      icon: 'mdi-star-plus',
      color: 'amber',
      type: 'rate'
    })
  }

  return baseButtons
})

const formatDuration = (minutes) => {
  if (!minutes) return 'N/A'
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return `${hours}ч ${mins}м`
}

const goToGenre = (genre) => {
  router.push({
    path: '/movies',
    query: { genre: genre.genre_id }
  })
}

const goToActor = (actor) => {
  console.log(actor)
  router.push(`/actor/${actor.id}`)
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
}

const handleImageError = () => {
  console.warn('Не удалось загрузить постер для фильма:', movieData.value?.title)
  imageError.value = true
}

const getDefaultPoster = () => {
  return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjQ1MCIgdmlld0JveD0iMCAwIDMwMCA0NTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSI0NTAiIGZpbGw9IiMxRDFFMjMiIHJ4PSI4Ii8+PHRleHQgeD0iMTUwIiB5PSIyMjAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgSGVscmV0aWNhLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE4IiBmaWxsPSIjRkZGIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXdlaWdodD0iNTAwIj5GaWxtIFBvc3RlcjwvdGV4dD48dGV4dCB4PSIxNTAiIHk9IjI0NSIgZm9udC1mYW1pbHk9IkFyaWFsLCBIZWx2ZXRpY2EsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiNGRkYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtd2VpZ2h0PSIzMDAiPk5vdCBhdmFpbGFibGU8L3RleHQ+PHBhdGggZD0iTTEwMCAxNTBIMjAwTTE1MCAxMDBWMjAwIiBzdHJva2U9IiNGRkYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PC9zdmc+'
}

const handleAction = async (type) => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }

  actionLoading.value[type] = true
  const filmId = route.params.id

  try {
    switch (type) {
      case 'favorite':
        if (isInFavorites.value) {
          await favoriteService.removeFilmFromFavorites(filmId)
        } else {
          await favoriteService.addFilmToFavorites(filmId)
        }
        isInFavorites.value = !isInFavorites.value
        break
        
      case 'watched':
        if (isWatched.value) {
          await watchedService.unmarkAsWatched(filmId)
        } else {
          await watchedService.markAsWatched(filmId)
        }
        isWatched.value = !isWatched.value
        break
        
      case 'rate':
        openRatingDialog()
        break
        
      case 'removeRating':
        await ratingService.removeRating(filmId)
        userRating.value = null
        await loadAverageRating()
        break
    }
  } catch (err) {
    console.error('Ошибка выполнения действия:', err)
  } finally {
    actionLoading.value[type] = false
  }
}

const openRatingDialog = async () => {
  const rating = prompt('Оцените фильм от 1 до 10:')
  if (rating && rating >= 1 && rating <= 10) {
    try {
      actionLoading.value.rate = true
      await ratingService.rateFilm(route.params.id, parseFloat(rating))
      userRating.value = parseFloat(rating)
      await loadAverageRating()
    } catch (err) {
      console.error('Ошибка оценки фильма:', err)
    } finally {
      actionLoading.value.rate = false
    }
  }
}

const loadMovieData = async () => {
  const movieId = route.params.id
  if (!movieId) return

  try {
    loading.value = true
    error.value = null
    imageError.value = false // сбрасываем ошибку изображения

    const [movieDataResponse, ratingData] = await Promise.all([
      movieService.getFilmDetails(movieId),
      ratingService.getAverageRating(movieId)
    ])

    // Сохраняем данные
    movieData.value = movieDataResponse
    averageRating.value = ratingData.avg_rating || 0

    if (movieDataResponse.stats?.ratings_count) {
      ratingsCount.value = movieDataResponse.stats.ratings_count
    }

    if (isAuthenticated.value) {
      await Promise.all([
        loadUserFavorites(),
        loadUserWatched(),
        loadUserRating()
      ])
    }
  } catch (err) {
    error.value = 'Не удалось загрузить данные фильма'
    console.error('Ошибка загрузки данных фильма:', err)
  } finally {
    loading.value = false
  }
}

const loadUserFavorites = async () => {
  try {
    isInFavorites.value = await favoriteService.checkFilmInFavorites(route.params.id)
  } catch (err) {
    console.error('Ошибка загрузки избранного:', err)
  }
}

const loadUserWatched = async () => {
  try {
    isWatched.value = await watchedService.checkIfWatched(route.params.id)
  } catch (err) {
    console.error('Ошибка загрузки просмотренных:', err)
  }
}

const loadUserRating = async () => {
  try {
    userRating.value = await ratingService.getUserRating(route.params.id)
  } catch (err) {
    console.error('Ошибка загрузки оценки пользователя:', err)
  }
}

const loadAverageRating = async () => {
  try {
    const ratingData = await ratingService.getAverageRating(route.params.id)
    averageRating.value = ratingData.avg_rating || 0
  } catch (err) {
    console.error('Ошибка загрузки среднего рейтинга:', err)
  }
}

onMounted(() => {
  loadMovieData()
})
</script>

<style scoped>
.poster-container {
  position: relative;
  max-width: 300px;
  margin: 0 auto;
}

.movie-poster {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.movie-poster:hover {
  transform: scale(1.02);
}

.movie-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
}

.movie-year {
  font-size: 1.5rem;
  color: #bdbdbd;
}

.movie-rating {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffd700;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #bdbdbd;
}

.movie-description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #e0e0e0;
  max-width: 800px;
}

h2, h3 {
  color: white;
  font-weight: 500;
}

:deep(.v-slide-group__content) {
  gap: 16px;
  padding: 8px 4px;
}
</style>