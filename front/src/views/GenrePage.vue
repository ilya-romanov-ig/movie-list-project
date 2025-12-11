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

    <v-row v-else-if="genre" class="mb-8">
      <v-col cols="12">
        <div class="d-flex align-center mb-4">
          <h1 class="genre-title">{{ genre.name }}</h1>
          <v-chip class="ml-4" color="primary" size="large">
            {{ genreFilms.length }} фильмов
          </v-chip>
        </div>

        <div class="mb-6">
          <v-text-field
            v-model="filmSearch"
            label="Поиск фильмов в жанре"
            clearable
            outlined
            color="white"
            prepend-inner-icon="mdi-movie-search"
            class="film-search-field"
            @input="filterFilms"
          />
        </div>

        <v-row>
          <v-col cols="12" md="8">
            <div class="mb-6">
              <h2 class="mb-4">Фильмы жанра</h2>
              
              <div v-if="filteredFilms.length === 0" class="text-center py-8">
                <v-icon size="64" class="mb-4">mdi-movie-off</v-icon>
                <p class="text-grey">Фильмы не найдены</p>
              </div>

              <v-row v-else>
                <v-col
                  v-for="movie in paginatedFilms"
                  :key="movie.film_id"
                  cols="12" sm="6" md="4" lg="3"
                >
                  <MovieCard 
                    :movie="movie" 
                    @click="goToMovie(movie.film_id)"
                  />
                </v-col>
              </v-row>

              <v-pagination
                v-if="filteredFilms.length > itemsPerPage"
                v-model="currentPage"
                :length="totalPages"
                class="mt-6"
                color="primary"
              />
            </div>
          </v-col>

          <v-col cols="12" md="4">
            <v-card class="mb-6" elevation="2">
              <v-card-title>Популярные в жанре</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item
                    v-for="movie in popularFilms"
                    :key="movie.film_id"
                    @click="goToMovie(movie.film_id)"
                    class="mb-2"
                  >
                    <template v-slot:prepend>
                      <v-icon>mdi-star</v-icon>
                    </template>
                    <v-list-item-title>{{ movie.title }}</v-list-item-title>
                    <v-list-item-subtitle>
                      Рейтинг: {{ movie.rating?.toFixed(1) || 'N/A' }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>

            <v-card elevation="2">
              <v-card-title>Статистика</v-card-title>
              <v-card-text>
                <v-list>
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon>mdi-film</v-icon>
                    </template>
                    <v-list-item-title>Всего фильмов</v-list-item-title>
                    <v-list-item-subtitle>{{ genreFilms.length }}</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon>mdi-trending-up</v-icon>
                    </template>
                    <v-list-item-title>Средний рейтинг</v-list-item-title>
                    <v-list-item-subtitle>{{ averageRating.toFixed(1) }}</v-list-item-subtitle>
                  </v-list-item>
                  
                  <v-list-item>
                    <template v-slot:prepend>
                      <v-icon>mdi-calendar</v-icon>
                    </template>
                    <v-list-item-title>Самый новый</v-list-item-title>
                    <v-list-item-subtitle>{{ newestFilmYear }}</v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-alert v-else-if="error" type="error" class="mb-8">
      {{ error }}
    </v-alert>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieCard from '@/components/MovieCard.vue'
import { useGenreService } from '@/services/genre.service'
import { useSearchService } from '@/services/search.service'
import { useMovieService } from '@/services/movie.service'

const router = useRouter()
const route = useRoute()

const genreService = useGenreService()
const searchService = useSearchService()
const movieService = useMovieService()

const searchQuery = ref('')
const filmSearch = ref('')
const loading = ref(true)
const error = ref(null)
const genre = ref(null)
const genreFilms = ref([])
const currentPage = ref(1)
const itemsPerPage = 12

const filteredFilms = computed(() => {
  if (!filmSearch.value) return genreFilms.value
  
  const searchTerm = filmSearch.value.toLowerCase()
  return genreFilms.value.filter(movie => 
    movie.title.toLowerCase().includes(searchTerm)
  )
})

const paginatedFilms = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredFilms.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredFilms.value.length / itemsPerPage)
})

const popularFilms = computed(() => {
  return [...genreFilms.value]
    .sort((a, b) => (b.rating || 0) - (a.rating || 0))
    .slice(0, 5)
})

const averageRating = computed(() => {
  if (genreFilms.value.length === 0) return 0
  const sum = genreFilms.value.reduce((acc, movie) => acc + (movie.rating || 0), 0)
  return sum / genreFilms.value.length
})

const newestFilmYear = computed(() => {
  if (genreFilms.value.length === 0) return 'N/A'
  const newest = genreFilms.value.reduce((newest, movie) => 
    (movie.year || 0) > (newest.year || 0) ? movie : newest
  )
  return newest.year || 'N/A'
})

const loadGenreData = async () => {
  const genreId = route.params.id
  if (!genreId) return

  try {
    loading.value = true
    error.value = null

    const [genreData, filmsData] = await Promise.all([
      genreService.getGenreDetails(genreId),
      genreService.getGenreFilms(genreId)
    ])

    genre.value = genreData
    genreFilms.value = filmsData.items || []

    // Загружаем дополнительную информацию о фильмах
    await loadFilmsDetails()
  } catch (err) {
    error.value = 'Не удалось загрузить данные жанра'
    console.error('Ошибка загрузки данных жанра:', err)
  } finally {
    loading.value = false
  }
}

const loadFilmsDetails = async () => {
  // TODO: Загрузить детали фильмов (рейтинги и т.д.)
  // Можно использовать batch запросы или загружать по одному
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/search',
      query: { q: searchQuery.value }
    })
  }
}

const filterFilms = () => {
  currentPage.value = 1 // Сбрасываем на первую страницу при фильтрации
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

onMounted(() => {
  loadGenreData()
})
</script>

<style scoped>
.genre-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
}

.film-search-field {
  max-width: 400px;
}

h2 {
  color: white;
  font-weight: 500;
  margin-bottom: 16px;
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

:deep(.v-pagination .v-btn) {
  color: white;
}
</style>