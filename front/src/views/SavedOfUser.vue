<template>
  <PageWrapper>
    <v-row justify="center" class="my-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          label="Поиск в сохранённом"
          clearable
          outlined
          color="white"
          prepend-inner-icon="mdi-magnify"
          class="search-field"
          @keyup.enter="performSearch"
        />
      </v-col>
    </v-row>

    <div v-if="loading" class="text-center my-8">
      <v-progress-circular indeterminate size="64" />
    </div>

    <div v-else>
      <h1 class="page-title mb-6">Моё сохранённое</h1>

      <v-tabs v-model="activeTab" color="primary" class="mb-6">
        <v-tab value="favorites">
          <v-icon start>mdi-heart</v-icon>
          Избранные фильмы ({{ favoriteMovies.length }})
        </v-tab>
        <v-tab value="watched">
          <v-icon start>mdi-eye</v-icon>
          Просмотренные ({{ watchedMovies.length }})
        </v-tab>
        <v-tab value="actors">
          <v-icon start>mdi-account-heart</v-icon>
          Любимые актёры ({{ favoriteActors.length }})
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <v-window-item value="favorites">
          <div v-if="filteredFavoriteMovies.length === 0" class="text-center py-8">
            <v-icon size="96" class="mb-4">mdi-heart-off</v-icon>
            <h3 class="mb-2">Нет избранных фильмов</h3>
            <p class="text-grey">Добавляйте фильмы в избранное, чтобы видеть их здесь</p>
            <v-btn color="primary" class="mt-4" to="/movies">
              <v-icon start>mdi-movie</v-icon>
              Найти фильмы
            </v-btn>
          </div>

          <v-row v-else>
            <v-col
              v-for="movie in filteredFavoriteMovies"
              :key="movie.film_id"
              cols="12" sm="6" md="4" lg="3"
            >
              <MovieCard 
                :movie="movie" 
                @click="goToMovie(movie.film_id)"
              />
            </v-col>
          </v-row>
        </v-window-item>

        <v-window-item value="watched">
          <div v-if="filteredWatchedMovies.length === 0" class="text-center py-8">
            <v-icon size="96" class="mb-4">mdi-eye-off</v-icon>
            <h3 class="mb-2">Нет просмотренных фильмов</h3>
            <p class="text-grey">Отмечайте фильмы как просмотренные, чтобы видеть их здесь</p>
          </div>

          <v-row v-else>
            <v-col
              v-for="movie in filteredWatchedMovies"
              :key="movie.film_id"
              cols="12" sm="6" md="4" lg="3"
            >
              <MovieCard 
                :movie="movie" 
                @click="goToMovie(movie.film_id)"
              />
            </v-col>
          </v-row>
        </v-window-item>

        <v-window-item value="actors">
          <div v-if="filteredFavoriteActors.length === 0" class="text-center py-8">
            <v-icon size="96" class="mb-4">mdi-account-off</v-icon>
            <h3 class="mb-2">Нет любимых актёров</h3>
            <p class="text-grey">Добавляйте актёров в избранное, чтобы видеть их здесь</p>
          </div>

          <v-row v-else>
            <v-col
              v-for="actor in filteredFavoriteActors"
              :key="actor.actor_id"
              cols="12" sm="6" md="4" lg="3"
            >
              <ActorCard 
                :actor="actor" 
                @click="goToActor(actor.actor_id)"
              />
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>
    </div>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieCard from '@/components/MovieCard.vue'
import ActorCard from '@/components/ActorCard.vue'
import { useFavoriteService } from '@/services/favorite.service'
import { useWatchedService } from '@/services/watched.service'

const router = useRouter()

const favoriteService = useFavoriteService()
const watchedService = useWatchedService()

const searchQuery = ref('')
const loading = ref(false)
const activeTab = ref('favorites')
const favoriteMovies = ref([])
const watchedMovies = ref([])
const favoriteActors = ref([])

const filteredFavoriteMovies = computed(() => {
  if (!searchQuery.value) return favoriteMovies.value
  const query = searchQuery.value.toLowerCase()
  return favoriteMovies.value.filter(movie => 
    movie.title?.toLowerCase().includes(query)
  )
})

const filteredWatchedMovies = computed(() => {
  if (!searchQuery.value) return watchedMovies.value
  const query = searchQuery.value.toLowerCase()
  return watchedMovies.value.filter(movie => 
    movie.title?.toLowerCase().includes(query)
  )
})

const filteredFavoriteActors = computed(() => {
  if (!searchQuery.value) return favoriteActors.value
  const query = searchQuery.value.toLowerCase()
  return favoriteActors.value.filter(actor => 
    actor.name?.toLowerCase().includes(query)
  )
})

const loadSavedData = async () => {
  try {
    loading.value = true
    
    const [favoritesData, watchedData, actorsData] = await Promise.all([
      favoriteService.getUserFavoriteFilms(),
      watchedService.getWatchedFilms(),
      favoriteService.getUserFavoriteActors()
    ])
    
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
    console.error('Ошибка загрузки сохранённого:', err)
  } finally {
    loading.value = false
  }
}

const performSearch = () => {
  // Поиск выполняется реактивно через computed свойства
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

const goToActor = (actorId) => {
  router.push(`/actor/${actorId}`)
}

onMounted(() => {
  loadSavedData()
})
</script>

<style scoped>
.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 24px;
}

.search-field {
  margin-bottom: 24px;
}

:deep(.v-tab) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.v-tab--selected) {
  color: white;
}
</style>