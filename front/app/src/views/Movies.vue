<template>
  <PageWrapper>
    <v-row justify="center" class="my-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          label="Поиск фильмов"
          clearable
          outlined
          color="white"
          prepend-inner-icon="mdi-magnify"
          class="search-field"
          @keyup.enter="performSearch"
        />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3" lg="2">
        <Filter
          v-model:filters="filters"
          @apply="loadMovies"
          @reset="resetSearch"
        />
      </v-col>

      <v-col cols="12" md="9" lg="10">
        <div v-if="loading" class="text-center my-8">
          <v-progress-circular indeterminate size="64" />
        </div>

        <div v-else>
          <div class="d-flex justify-space-between align-center mb-4">
            <h1 class="page-title">Фильмы</h1>
            <div class="d-flex align-center">
              <span class="mr-4 text-grey">{{ totalItems }} фильмов</span>
            </div>
          </div>

          <v-row v-if="movies.length === 0" class="mb-8">
            <v-col cols="12" class="text-center">
              <v-icon size="96" class="mb-4">mdi-movie-off</v-icon>
              <h3 class="mb-2">Фильмы не найдены</h3>
              <p class="text-grey">Попробуйте изменить параметры поиска</p>
            </v-col>
          </v-row>

          <v-row v-else>
            <v-col
              v-for="movie in movies"
              :key="movie.id || movie.film_id"
              cols="12" sm="6" md="4" lg="3" xl="2"
            >
              <MovieCard 
                :movie="movie" 
                @click="goToMovie(movie.id || movie.film_id)"
              />
            </v-col>
          </v-row>

          <v-pagination
            v-if="totalPages > 1"
            v-model="currentPage"
            :length="totalPages"
            class="mt-6"
            color="primary"
          />
        </div>
      </v-col>
    </v-row>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieCard from '@/components/MovieCard.vue'
import Filter from '@/components/Filter.vue'
import { useMovieService } from '@/services/movie.service'
import { useSearchService } from '@/services/search.service'

const router = useRouter()
const route = useRoute()

const movieService = useMovieService()
const searchService = useSearchService()

const searchQuery = ref('')
const loading = ref(false)
const movies = ref([])
const currentPage = ref(1)
const itemsPerPage = 24
const totalItems = ref(0)

const filters = ref({
  genre: null,
  year: null,
  actor: null,
  sortBy: 'rating_desc',
  ratingRange: [0, 10]
})

const totalPages = computed(() => {
  return Math.ceil(totalItems.value / itemsPerPage)
})

const loadMovies = async () => {
  try {
    loading.value = true
    
    const params = {
      limit: itemsPerPage,
      offset: (currentPage.value - 1) * itemsPerPage,
    }
    
    // Добавляем поиск
    if (searchQuery.value) {
      params.q = searchQuery.value
    }
    
    // Добавляем фильтры
    if (filters.value.genre) {
      params.genre_id = filters.value.genre
    }
    if (filters.value.year) {
      params.year = filters.value.year
    }
    if (filters.value.actor) {
      params.actor_id = filters.value.actor
    }
    if (filters.value.ratingRange[0] > 0 || filters.value.ratingRange[1] < 10) {
      params.min_rating = filters.value.ratingRange[0]
      params.max_rating = filters.value.ratingRange[1]
    }
    
    // Добавляем сортировку
    switch (filters.value.sortBy) {
      case 'rating_desc':
        params.sort = '-rating'
        break
      case 'rating_asc':
        params.sort = 'rating'
        break
      case 'year_desc':
        params.sort = '-year'
        break
      case 'year_asc':
        params.sort = 'year'
        break
      case 'title_asc':
        params.sort = 'title'
        break
      case 'title_desc':
        params.sort = '-title'
        break
    }
    
    // Используем поиск как основной метод
    const searchResults = await searchService.searchFilms(searchQuery.value || '', params)
    movies.value = searchResults.items || []
    totalItems.value = searchResults.count || 0
  } catch (err) {
    console.error('Ошибка загрузки фильмов:', err)
  } finally {
    loading.value = false
  }
}

const performSearch = () => {
  currentPage.value = 1
  loadMovies()
}

const resetSearch = () => {
  searchQuery.value = ''
  filters.value = {
    genre: null,
    year: null,
    actor: null,
    sortBy: 'rating_desc',
    ratingRange: [0, 10]
  }
  currentPage.value = 1
  loadMovies()
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

// Реакция на изменение страницы
watch(currentPage, () => {
  loadMovies()
})

// Реакция на изменение query параметров
watch(() => route.query, (newQuery) => {
  if (newQuery.genre) {
    filters.value.genre = parseInt(newQuery.genre)
  }
  if (newQuery.actor) {
    filters.value.actor = newQuery.actor
  }
  if (newQuery.q) {
    searchQuery.value = newQuery.q
  }
  
  loadMovies()
}, { immediate: true })

onMounted(() => {
  loadMovies()
})
</script>

<style scoped>
.page-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
}

.search-field {
  margin-bottom: 24px;
}

:deep(.v-pagination .v-btn) {
  color: white;
}
</style>