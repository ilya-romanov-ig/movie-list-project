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

    <div v-else>
      <v-row class="mb-8">
        <v-col cols="12">
          <h1 class="profile-title">Профиль пользователя</h1>
          <div class="user-info mb-6">
            <v-icon size="64" class="mr-4">mdi-account-circle</v-icon>
            <div>
              <h2 class="user-name">{{ user?.username || 'Пользователь' }}</h2>
              <p class="user-email text-grey">{{ user?.email }}</p>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <v-card class="mb-6" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Просмотренные фильмы</span>
              <v-chip color="primary">{{ watchedMovies.length }}</v-chip>
            </v-card-title>
            <v-card-text>
              <v-list v-if="watchedMovies.length > 0">
                <v-list-item
                  v-for="movie in watchedMovies"
                  :key="movie.film_id"
                  @click="goToMovie(movie.film_id)"
                  class="mb-2"
                >
                  <template v-slot:prepend>
                    <v-icon>mdi-eye</v-icon>
                  </template>
                  <v-list-item-title>{{ movie.title }}</v-list-item-title>
                  <template v-slot:append>
                    <v-btn icon variant="text" @click.stop="removeFromWatched(movie.film_id)">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info">
                Нет просмотренных фильмов
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card class="mb-6" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Избранные фильмы</span>
              <v-chip color="primary">{{ favoriteMovies.length }}</v-chip>
            </v-card-title>
            <v-card-text>
              <v-list v-if="favoriteMovies.length > 0">
                <v-list-item
                  v-for="movie in favoriteMovies"
                  :key="movie.film_id"
                  @click="goToMovie(movie.film_id)"
                  class="mb-2"
                >
                  <template v-slot:prepend>
                    <v-icon color="red">mdi-heart</v-icon>
                  </template>
                  <v-list-item-title>{{ movie.title }}</v-list-item-title>
                  <template v-slot:append>
                    <v-btn icon variant="text" @click.stop="removeFromFavorites(movie.film_id)">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info">
                Нет избранных фильмов
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <v-card class="mb-6" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Избранные актёры</span>
              <v-chip color="primary">{{ favoriteActors.length }}</v-chip>
            </v-card-title>
            <v-card-text>
              <v-list v-if="favoriteActors.length > 0">
                <v-list-item
                  v-for="actor in favoriteActors"
                  :key="actor.actor_id"
                  @click="goToActor(actor.actor_id)"
                  class="mb-2"
                >
                  <template v-slot:prepend>
                    <v-icon color="red">mdi-heart</v-icon>
                  </template>
                  <v-list-item-title>{{ actor.name }}</v-list-item-title>
                  <template v-slot:append>
                    <v-btn icon variant="text" @click.stop="removeActorFromFavorites(actor.actor_id)">
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
              <v-alert v-else type="info">
                Нет избранных актёров
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>

        <v-col cols="12" md="6">
          <v-card class="mb-6" elevation="2">
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Статистика</span>
            </v-card-title>
            <v-card-text>
              <v-list>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon>mdi-film</v-icon>
                  </template>
                  <v-list-item-title>Всего фильмов просмотрено</v-list-item-title>
                  <v-list-item-subtitle>{{ watchedMovies.length }}</v-list-item-subtitle>
                </v-list-item>
                
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="red">mdi-heart</v-icon>
                  </template>
                  <v-list-item-title>Фильмов в избранном</v-list-item-title>
                  <v-list-item-subtitle>{{ favoriteMovies.length }}</v-list-item-subtitle>
                </v-list-item>
                
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="red">mdi-heart</v-icon>
                  </template>
                  <v-list-item-title>Актёров в избранном</v-list-item-title>
                  <v-list-item-subtitle>{{ favoriteActors.length }}</v-list-item-subtitle>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import { useFavoriteService } from '@/services/favorite.service'
import { useWatchedService } from '@/services/watched.service'
import { useAuthStore } from '@/stores/auth'
import { useSearchService } from '@/services/search.service'
import { useUserService } from '@/services/user.service'

const router = useRouter()
const authStore = useAuthStore()

const favoriteService = useFavoriteService()
const watchedService = useWatchedService()
const searchService = useSearchService()
const userService = useUserService()

const searchQuery = ref('')
const loading = ref(true)
const user = ref(null)
const watchedMovies = ref([])
const favoriteMovies = ref([])
const favoriteActors = ref([])

const loadProfileData = async () => {
  try {
    loading.value = true

    const userId = authStore.userId
    if (!userId) {
      router.push('/login')
      return
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
    
    // Для просмотренных нужно получить детали фильмов
    if (watchedData.film_ids?.length > 0) {
      // TODO: Загрузить детали фильмов по ID
      watchedMovies.value = watchedData.film_ids.map(id => ({
        film_id: id,
        title: `Фильм ${id}` // Временная заглушка
      }))
    }
  } catch (err) {
    console.error('Ошибка загрузки профиля:', err)
  } finally {
    loading.value = false
  }
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
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
.profile-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 24px;
}

.user-info {
  display: flex;
  align-items: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.user-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  margin-bottom: 4px;
}

.user-email {
  font-size: 1rem;
}

:deep(.v-card-title) {
  color: white;
  font-weight: 500;
}

:deep(.v-list-item) {
  cursor: pointer;
  transition: background-color 0.2s;
}

:deep(.v-list-item:hover) {
  background-color: rgba(255, 255, 255, 0.05);
}

:deep(.v-list-item-title) {
  color: white;
}

:deep(.v-list-item-subtitle) {
  color: #bdbdbd;
}
</style>