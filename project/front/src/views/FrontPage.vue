<template>
  <PageWrapper>
    <v-row justify="center" class="my-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          :label="`Поиск по ${searchMode}`"
          clearable
          outlined
          color="white"
          class="search-field"
          @keydown.enter="performSearch"
          @click:clear="clearSearch"
        >
          <template #append>
            <v-select
              v-model="searchMode"
              :items="searchModes"
              dense
              outlined
              hide-details
              color="white"
              class="mode-select"
              item-color="grey"
            />
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <div v-if="loading" class="text-center my-8">
      <v-progress-circular indeterminate size="64" />
    </div>

    <!-- Результаты поиска актеров -->
    <div v-if="searchResults.actors.length > 0 && searchQuery.trim() && searchMode === 'актерам'" class="actors-results">
      <v-row class="mb-6">
        <v-col cols="12">
          <h2 class="text-h5 mb-4">Найденные актеры</h2>
        </v-col>
        <v-col
          v-for="actor in searchResults.actors"
          :key="actor.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card
            class="actor-card"
            @click="goToActor(actor.id)"
          >
            <v-img
              v-if="actor.photo_url"
              :src="actor.photo_url"
              :alt="actor.name"
              height="200px"
              cover
            />
            <v-img
              v-else
              src="@/assets/default-actor.jpg"
              alt="Default actor"
              height="200px"
              cover
            />
            <v-card-title class="text-subtitle-1 font-weight-medium">
              {{ actor.name }}
            </v-card-title>
            <v-card-subtitle v-if="actor.birth_date" class="text-caption">
              {{ formatDate(actor.birth_date) }}
            </v-card-subtitle>
            <v-card-subtitle v-if="actor.country" class="text-caption">
              {{ actor.country }}
            </v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <!-- Результаты поиска фильмов -->
    <div v-else-if="searchResults.films.length > 0 && searchQuery.trim() && searchMode === 'фильмам'" class="films-results">
      <MovieSection 
        title="Результаты поиска" 
        :movies="searchResults.films" 
      />
    </div>

    <!-- Основные секции (показываются только когда нет активного поиска) -->
    <div v-else-if="!searchQuery.trim()">
      <MovieSection 
        v-if="homeData.top_films?.items?.length"
        title="Высокий рейтинг" 
        :movies="homeData.top_films.items" 
      />

      <MovieSection 
        v-if="homeData.newest_films?.items?.length"
        title="Новинки" 
        :movies="homeData.newest_films.items" 
      />

      <MovieSection 
        v-if="homeData.recommended?.items?.length"
        title="Рекомендовано для вас" 
        :movies="homeData.recommended.items" 
      />

      <MovieSection 
        v-if="homeData.trending?.items?.length"
        title="Популярное сейчас" 
        :movies="homeData.trending.items" 
      />

      <v-alert v-if="!hasMovies" type="info" class="my-8">
        Фильмы не найдены. Попробуйте обновить страницу.
      </v-alert>
    </div>

    <!-- Сообщение, если ничего не найдено -->
    <div v-else-if="searchQuery.trim() && !loading" class="text-center my-8">
      <v-alert type="info">
        По запросу "{{ searchQuery }}" ничего не найдено
      </v-alert>
    </div>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieSection from '@/components/MovieSection.vue'
import { useCombinedMoviesService } from '@/services/front_page.service'
import { useSearchService } from '@/services/search.service'
import { useActorService } from '@/services/actor.service'

const router = useRouter()
const combinedService = useCombinedMoviesService()
const searchService = useSearchService()
const actorService = useActorService()

const searchQuery = ref('')
const searchMode = ref('фильмам')
const loading = ref(false)
const homeData = ref({
  top_films: { items: [] },
  newest_films: { items: [] },
  recommended: { items: [] },
  trending: { items: [] }
})

const searchResults = ref({
  films: [],
  actors: []
})

const searchModes = [
  { title: 'фильмам', value: 'фильмам' },
  { title: 'актерам', value: 'актерам' },
]

const hasMovies = computed(() => {
  return (
    homeData.value.top_films?.items?.length > 0 ||
    homeData.value.newest_films?.items?.length > 0 ||
    homeData.value.recommended?.items?.length > 0 ||
    homeData.value.trending?.items?.length > 0
  )
})

// Функция для форматирования даты
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

// Навигация к странице актера
const goToActor = (actorId) => {
  router.push(`/actor/${actorId}`)
}

const loadHomeData = async () => {
  try {
    loading.value = true
    const data = await combinedService.getAllHomeMoviesWithDetails()
    
    homeData.value = {
      top_films: data.top_films || { items: [] },
      newest_films: data.newest_films || { items: [] },
      recommended: data.recommended || { items: [] },
      trending: data.trending || { items: [] }
    }
    
    // Очищаем результаты поиска
    searchResults.value = { films: [], actors: [] }
  } catch (error) {
    console.error('Ошибка загрузки главной страницы:', error)
  } finally {
    loading.value = false
  }
}

const performSearch = async () => {
  if (!searchQuery.value.trim()) {
    await loadHomeData()
    return
  }
  
  try {
    loading.value = true
    
    if (searchMode.value === 'фильмам') {
      // Поиск фильмов
      const results = await searchService.search(searchQuery.value)
      const films = results.results?.films || []
      
      if (films.length === 0) {
        searchResults.value = { films: [], actors: [] }
        return
      }
      
      const filmIds = films.map(film => film.id)
      
      try {
        const data = await combinedService.getMoviesByIds(filmIds)
        searchResults.value = {
          films: data || [],
          actors: []
        }
      } catch (getMoviesError) {
        console.error('Ошибка получения деталей фильмов:', getMoviesError)
        searchResults.value = { films: [], actors: [] }
      }
      
    } else if (searchMode.value === 'актерам') {
      // Поиск актеров
      try {
        const results = await actorService.searchActors(searchQuery.value)
        
        let actors = []
        if (Array.isArray(results)) {
          actors = results
        } else if (results?.items) {
          actors = results.items
        } else if (results?.results?.actors) {
          actors = results.results.actors
        } else if (results?.actors) {
          actors = results.actors
        }
        
        searchResults.value = {
          films: [],
          actors: actors || []
        }
        
      } catch (actorError) {
        console.error('Ошибка поиска актеров:', actorError)
        searchResults.value = { films: [], actors: [] }
      }
    }
    
  } catch (error) {
    console.error('❌ Общая ошибка поиска:', error)
    searchResults.value = { films: [], actors: [] }
  } finally {
    loading.value = false
  }
}

const clearSearch = async () => {
  searchQuery.value = ''
  await loadHomeData()
}

// Автоматический поиск при изменении запроса (с debounce)
let searchTimeout = null
watch([searchQuery, searchMode], () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  
  searchTimeout = setTimeout(() => {
    if (searchQuery.value.trim()) {
      performSearch()
    } else {
      loadHomeData()
    }
  }, 500) // 500ms debounce
})

onMounted(() => {
  loadHomeData()
})
</script>

<style scoped>
.mode-select {
  max-width: 150px;
}

.search-field {
  margin-bottom: 24px;
}

.actors-results {
  margin-top: 24px;
}

.actor-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.actor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.actor-card .v-card-title {
  padding: 12px 16px 4px;
  line-height: 1.3;
  word-break: break-word;
}

.actor-card .v-card-subtitle {
  padding: 0 16px 8px;
}
</style>