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

    <v-row v-else-if="actor" class="mb-8">
      <v-col cols="12" md="4" lg="3">
        <v-img
          :src="actor.photo_url"
          aspect-ratio="2/3"
          class="actor-poster elevation-6"
          rounded
        >
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular indeterminate color="grey lighten-5" />
            </v-row>
          </template>
        </v-img>
      </v-col>

      <v-col cols="12" md="8" lg="9">
        <div class="d-flex align-center mb-2">
          <h1 class="actor-title">{{ actor.name }}</h1>
        </div>

        <div class="mb-4">
          <v-chip class="mr-2 mb-2" color="primary">
            <v-icon start>mdi-cake</v-icon>
            {{ actor.birth_year || 'Дата рождения неизвестна' }}
          </v-chip>
          
          <v-chip class="mr-2 mb-2" color="primary" v-if="actor.death_year">
            <v-icon start>mdi-cross</v-icon>
            {{ actor.death_year }}
          </v-chip>
        </div>

        <v-row class="mb-6">
          <v-col cols="6" md="4" lg="3">
            <div class="stat-item">
              <div class="stat-value">{{ favoritesCount?.toLocaleString() || 0 }}</div>
              <div class="stat-label">В избранном</div>
            </div>
          </v-col>
        </v-row>

        <div class="mb-6">
          <v-row>
            <v-col cols="12" sm="6" md="4" lg="3">
              <v-btn
                :color="isInFavorites ? 'error' : 'primary'"
                block
                :prepend-icon="isInFavorites ? 'mdi-heart' : 'mdi-heart-outline'"
                @click="toggleFavorite"
                variant="outlined"
                :loading="favoriteLoading"
                :disabled="!isAuthenticated"
              >
                {{ isInFavorites ? 'Удалить из избранного' : 'Добавить в избранное' }}
              </v-btn>
            </v-col>
            
            <v-col cols="12" sm="6" md="4" lg="3">
              <v-btn
                color="secondary"
                block
                prepend-icon="mdi-filmstrip"
                @click="goToAllFilms"
                variant="outlined"
              >
                Все фильмы
              </v-btn>
            </v-col>
          </v-row>
        </div>

        <div class="mb-8" v-if="actor.bio">
          <h3 class="mb-2">Биография</h3>
          <p class="actor-bio">{{ actor.bio }}</p>
        </div>
      </v-col>
    </v-row>

    <v-alert v-else-if="error" type="error" class="mb-8">
      {{ error }}
    </v-alert>

    <div v-if="filmography.length > 0" class="mb-8">
      <h2 class="mb-4">Фильмография</h2>
      <v-slide-group show-arrows>
        <v-slide-item v-for="movie in filmography" :key="movie.film_id">
          <MovieCard 
            :movie="movie" 
            class="mx-3"
            @click="goToMovie(movie.film_id)"
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
import { useActorService } from '@/services/actor.service'
import { useFavoriteService } from '@/services/favorite.service'
import { useCombinedMoviesService } from '@/services/front_page.service'
import { useAuthStore } from '@/stores/auth'
import { useSearchService } from '@/services/search.service'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const actorService = useActorService()
const favoriteService = useFavoriteService()
const combinedService = useCombinedMoviesService()
const searchService = useSearchService()

const searchQuery = ref('')
const loading = ref(true)
const error = ref(null)
const actor = ref(null)
const filmography = ref([])
const favoritesCount = ref(0)
const isInFavorites = ref(false)
const favoriteLoading = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)

const loadActorData = async () => {
  const actorId = route.params.id
  if (!actorId) return

  try {
    loading.value = true
    error.value = null

    const [actorData, filmsData] = await Promise.all([
      actorService.getActorDetails(actorId),
      actorService.getActorFilms(actorId)
    ])

    actor.value = actorData
    
    const basicFilms = filmsData.items?.slice(0, 5) || []
    filmography.value = await combinedService.enrichActorFilmography(basicFilms)

    if (isAuthenticated.value) {
      await loadUserFavorites()
    }
  } catch (err) {
    error.value = 'Не удалось загрузить данные актёра'
    console.error('Ошибка загрузки данных актёра:', err)
  } finally {
    loading.value = false
  }
}

const loadUserFavorites = async () => {
  try {
    isInFavorites.value = await favoriteService.checkActorInFavorites(route.params.id)
  } catch (err) {
    console.error('Ошибка загрузки избранного:', err)
  }
}

const toggleFavorite = async () => {
  if (!isAuthenticated.value) {
    router.push('/login')
    return
  }

  favoriteLoading.value = true
  const actorId = route.params.id

  try {
    if (isInFavorites.value) {
      await favoriteService.removeActorFromFavorites(actorId)
    } else {
      await favoriteService.addActorToFavorites(actorId)
    }
    isInFavorites.value = !isInFavorites.value
  } catch (err) {
    console.error('Ошибка изменения избранного:', err)
  } finally {
    favoriteLoading.value = false
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

const goToAllFilms = () => {
  const actorId = route.params.id
  router.push({
    path: '/movies',
    query: { actor: actorId }
  })
}

onMounted(() => {
  loadActorData()
})
</script>

<style scoped>
.actor-poster {
  max-width: 300px;
  margin: 0 auto;
}

.actor-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
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

.actor-bio {
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