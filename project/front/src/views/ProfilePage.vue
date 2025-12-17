<template>
  <PageWrapper>
    <v-row justify="center" class="mb-8">
      <v-col cols="12" md="8">
        <v-card class="profile-header-card" elevation="4">
          <v-card-text class="pa-6">
            <div class="d-flex align-center">
              <v-avatar size="80" class="mr-4">
                <v-icon size="64">mdi-account-circle</v-icon>
              </v-avatar>
              <div>
                <h1 class="text-h5 font-weight-bold mb-2">{{ user?.username || 'Пользователь' }}</h1>
                <p class="text-body-1 text-medium-emphasis mb-0">{{ user?.email }}</p>
                <div class="d-flex align-center mt-2">
                  <v-chip size="small" color="primary" class="mr-2">
                    <v-icon start size="small">mdi-calendar</v-icon>
                    Зарегистрирован: {{ formatDate(user?.created_at) }}
                  </v-chip>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="loading" class="mb-8">
      <v-col cols="12" class="text-center">
        <v-progress-circular indeterminate size="64" />
      </v-col>
    </v-row>

    <div v-else>

      <!-- Секции с данными -->
      <v-row>
        <!-- Просмотренные фильмы -->
        <v-col cols="12" md="6">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center py-4 px-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2" color="blue">mdi-eye</v-icon>
                <span>Просмотренные фильмы</span>
              </div>
              <v-chip color="primary" variant="elevated">{{ watchedMovies.length }}</v-chip>
            </v-card-title>
            <v-divider />
            <v-card-text class="pa-0">
              <v-list v-if="watchedMovies.length > 0" class="pa-0">
                <v-list-item
                  v-for="movie in watchedMovies"
                  :key="movie.film_id"
                  :title="movie.title"
                  @click="goToMovie(movie.film_id)"
                  class="py-3 px-4"
                >
                  <template v-slot:prepend>
                    <v-avatar size="40" rounded class="mr-3">
                      <v-img v-if="movie.poster_url" :src="movie.poster_url" />
                      <v-icon v-else>mdi-film</v-icon>
                    </v-avatar>
                  </template>
                  
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    {{ movie.title }}
                  </v-list-item-title>
                  
                  <template v-slot:append>
                    <div class="d-flex align-center">
                      <v-rating
                        v-if="movie.rating"
                        :model-value="movie.rating"
                        size="small"
                        readonly
                        color="amber"
                        density="compact"
                        half-increments
                      />
                      <v-btn
                        icon
                        variant="text"
                        size="small"
                        @click.stop="removeFromWatched(movie.film_id)"
                        class="ml-2"
                      >
                        <v-icon size="small">mdi-close</v-icon>
                      </v-btn>
                    </div>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="pa-4 text-center">
                <v-icon size="64" color="grey" class="mb-2">mdi-film-off</v-icon>
                <p class="text-body-1 text-medium-emphasis">Нет просмотренных фильмов</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Избранные фильмы -->
        <v-col cols="12" md="6">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center py-4 px-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2" color="red">mdi-heart</v-icon>
                <span>Избранные фильмы</span>
              </div>
              <v-chip color="red" variant="elevated">{{ favoriteMovies.length }}</v-chip>
            </v-card-title>
            <v-divider />
            <v-card-text class="pa-0">
              <v-list v-if="favoriteMovies.length > 0" class="pa-0">
                <v-list-item
                  v-for="movie in favoriteMovies"
                  :key="movie.film_id"
                  :title="movie.title"
                  @click="goToMovie(movie.film_id)"
                  class="py-3 px-4"
                >
                  <template v-slot:prepend>
                    <v-avatar size="40" rounded class="mr-3">
                      <v-img v-if="movie.poster_url" :src="movie.poster_url" />
                      <v-icon v-else>mdi-film</v-icon>
                    </v-avatar>
                  </template>
                  
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    {{ movie.title }}
                  </v-list-item-title>
                  
                  <template v-slot:append>
                    <div class="d-flex align-center">
                      <v-rating
                        v-if="movie.rating"
                        :model-value="movie.rating"
                        size="small"
                        readonly
                        color="amber"
                        density="compact"
                        half-increments
                      />
                      <v-btn
                        icon
                        variant="text"
                        size="small"
                        @click.stop="removeFromFavorites(movie.film_id)"
                        class="ml-2"
                      >
                        <v-icon size="small">mdi-close</v-icon>
                      </v-btn>
                    </div>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="pa-4 text-center">
                <v-icon size="64" color="grey" class="mb-2">mdi-heart-off</v-icon>
                <p class="text-body-1 text-medium-emphasis">Нет избранных фильмов</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Избранные актёры -->
        <v-col cols="12" md="6">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center py-4 px-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2" color="red">mdi-heart</v-icon>
                <span>Избранные актёры</span>
              </div>
              <v-chip color="red" variant="elevated">{{ favoriteActors.length }}</v-chip>
            </v-card-title>
            <v-divider />
            <v-card-text class="pa-0">
              <v-list v-if="favoriteActors.length > 0" class="pa-0">
                <v-list-item
                  v-for="actor in favoriteActors"
                  :key="actor.actor_id"
                  :title="actor.name"
                  @click="goToActor(actor.actor_id)"
                  class="py-3 px-4"
                >
                  <template v-slot:prepend>
                    <v-avatar size="40" rounded class="mr-3">
                      <v-img v-if="actor.photo_url" :src="actor.photo_url" />
                      <v-icon v-else>mdi-account</v-icon>
                    </v-avatar>
                  </template>
                  
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    {{ actor.name }}
                  </v-list-item-title>
                  
                  <v-list-item-subtitle v-if="actor.birth_date || actor.country" class="text-caption">
                    {{ actor.birth_date ? formatDate(actor.birth_date) : '' }}
                    {{ actor.country ? ` • ${actor.country}` : '' }}
                  </v-list-item-subtitle>
                  
                  <template v-slot:append>
                    <v-btn
                      icon
                      variant="text"
                      size="small"
                      @click.stop="removeActorFromFavorites(actor.actor_id)"
                    >
                      <v-icon size="small">mdi-close</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <div v-else class="pa-4 text-center">
                <v-icon size="64" color="grey" class="mb-2">mdi-account-off</v-icon>
                <p class="text-body-1 text-medium-emphasis">Нет избранных актёров</p>
              </div>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Статистика -->
        <v-col cols="12" md="6">
          <v-card class="mb-4" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center py-4 px-4">
              <div class="d-flex align-center">
                <v-icon class="mr-2" color="green">mdi-chart-bar</v-icon>
                <span>Статистика</span>
              </div>
              <v-icon color="green">mdi-information</v-icon>
            </v-card-title>
            <v-divider />
            <v-card-text class="pa-4">
              <v-list class="pa-0">
                <v-list-item class="px-0">
                  <template v-slot:prepend>
                    <v-avatar color="blue" size="40" rounded class="mr-3">
                      <v-icon color="white">mdi-film</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    Всего фильмов просмотрено
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-2 text-medium-emphasis">
                    {{ watchedMovies.length }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-divider class="my-3" />

                <v-list-item class="px-0">
                  <template v-slot:prepend>
                    <v-avatar color="red" size="40" rounded class="mr-3">
                      <v-icon color="white">mdi-heart</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    Фильмов в избранном
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-2 text-medium-emphasis">
                    {{ favoriteMovies.length }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-divider class="my-3" />

                <v-list-item class="px-0">
                  <template v-slot:prepend>
                    <v-avatar color="red" size="40" rounded class="mr-3">
                      <v-icon color="white">mdi-heart</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    Актёров в избранном
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-2 text-medium-emphasis">
                    {{ favoriteActors.length }}
                  </v-list-item-subtitle>
                </v-list-item>

                <v-divider class="my-3" />

                <v-list-item class="px-0">
                  <template v-slot:prepend>
                    <v-avatar color="amber" size="40" rounded class="mr-3">
                      <v-icon color="white">mdi-star</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-1 font-weight-medium">
                    Средний рейтинг
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-2 text-medium-emphasis">
                    {{ averageRating }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </PageWrapper>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import { useFavoriteService } from '@/services/favorite.service'
import { useWatchedService } from '@/services/watched.service'
import { useAuthStore } from '@/stores/auth'
import { useUserService } from '@/services/user.service'
import { useMovieService } from '@/services/movie.service'

const router = useRouter()
const authStore = useAuthStore()

const favoriteService = useFavoriteService()
const watchedService = useWatchedService()
const userService = useUserService()
const movieService = useMovieService()

const loading = ref(true)
const user = ref(null)
const watchedMovies = ref([])
const favoriteMovies = ref([])
const favoriteActors = ref([])

const averageRating = computed(() => {
  const ratings = watchedMovies.value
    .filter(movie => movie.rating)
    .map(movie => movie.rating)
  
  if (ratings.length === 0) return '—'
  
  const avg = ratings.reduce((sum, rating) => sum + rating, 0) / ratings.length
  return avg.toFixed(1)
})

const formatDate = (dateString) => {
  if (!dateString) return '—'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU')
  } catch {
    return dateString
  }
}

const loadProfileData = async () => {
  try {
    loading.value = true

    const userId = authStore.userId
    if (!userId) {
      router.push('/login')
      return
    }

    // Загружаем данные параллельно
    const [userData, favoritesData, watchedData, actorsData] = await Promise.all([
      userService.getUser(userId),
      favoriteService.getUserFavoriteFilms(),
      watchedService.getWatchedFilms(),
      favoriteService.getUserFavoriteActors()
    ])

    user.value = userData
    favoriteActors.value = actorsData.items || []
    
    // Загружаем детали фильмов для избранного
    if (favoritesData.items?.length > 0) {
      const filmDetails = await movieService.getMoviesByIds(favoritesData.items.map(f => f.film_id))
      favoriteMovies.value = filmDetails || []
    } else {
      favoriteMovies.value = []
    }
    
    // Загружаем детали просмотренных фильмов
    if (watchedData.film_ids?.length > 0) {
      const watchedDetails = await movieService.getMoviesByIds(watchedData.film_ids)
      watchedMovies.value = watchedDetails || []
    } else {
      watchedMovies.value = []
    }
    
  } catch (err) {
    console.error('Ошибка загрузки профиля:', err)
  } finally {
    loading.value = false
  }
}

// const performSearch = () => {
//   if (searchQuery.value.trim()) {
//     router.push({
//       path: '/search',
//       query: { q: searchQuery.value }
//     })
//   }
// }

const clearSearch = () => {
  searchQuery.value = ''
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

const goToActor = (actorId) => {
  router.push(`/actor/${actorId}`)
}

const removeFromWatched = async (movieId) => {
  try {
    await watchedService.unmarkAsWatched(movieId)
    watchedMovies.value = watchedMovies.value.filter(m => m.film_id !== movieId)
  } catch (err) {
    console.error('Ошибка удаления из просмотренных:', err)
  }
}

const removeFromFavorites = async (movieId) => {
  try {
    await favoriteService.removeFilmFromFavorites(movieId)
    favoriteMovies.value = favoriteMovies.value.filter(m => m.film_id !== movieId)
  } catch (err) {
    console.error('Ошибка удаления из избранного:', err)
  }
}

const removeActorFromFavorites = async (actorId) => {
  try {
    await favoriteService.removeActorFromFavorites(actorId)
    favoriteActors.value = favoriteActors.value.filter(a => a.actor_id !== actorId)
  } catch (err) {
    console.error('Ошибка удаления актёра из избранного:', err)
  }
}

onMounted(() => {
  loadProfileData()
})
</script>

<style scoped>
/* Профиль будет использовать тему Vuetify */
.profile-header-card {
  border-radius: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, #66ea85 20%, #5f06b9 80%);
}

.profile-header-card :deep(.v-card-text) {
  color: white;
}

/* Анимации для карточек */
.v-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.v-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.2);
}

/* Стили для списков */
.v-list-item {
  border-radius: 8px;
  margin: 4px 0;
}

.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.08);
}

/* Аватарки */
.v-avatar {
  border: 2px solid rgba(var(--v-theme-primary), 0.3);
}

/* Чипы */
.v-chip {
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Разделители */
.v-divider {
  opacity: 0.2;
}
</style>