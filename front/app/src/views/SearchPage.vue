<template>
  <PageWrapper>
    <v-row justify="center" class="my-4">
      <v-col cols="12" md="8">
        <v-text-field
          v-model="searchQuery"
          label="Поиск по фильмам, актёрам, пользователям"
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
      <div class="d-flex justify-space-between align-center mb-6">
        <h1 class="page-title">
          Результаты поиска: "{{ searchQuery }}"
        </h1>
        <v-chip color="primary" size="large">
          {{ totalResults }} найдено
        </v-chip>
      </div>

      <v-tabs v-model="activeTab" color="primary" class="mb-6">
        <v-tab value="films">
          <v-icon start>mdi-film</v-icon>
          Фильмы ({{ results.films?.length || 0 }})
        </v-tab>
        <v-tab value="actors">
          <v-icon start>mdi-account</v-icon>
          Актёры ({{ results.actors?.length || 0 }})
        </v-tab>
        <v-tab value="users">
          <v-icon start>mdi-account-group</v-icon>
          Пользователи ({{ results.users?.length || 0 }})
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <v-window-item value="films">
          <div v-if="results.films?.length === 0" class="text-center py-8">
            <v-icon size="96" class="mb-4">mdi-movie-off</v-icon>
            <h3 class="mb-2">Фильмы не найдены</h3>
            <p class="text-grey">Попробуйте изменить запрос поиска</p>
          </div>

          <v-row v-else>
            <v-col
              v-for="movie in results.films"
              :key="movie.id || movie.film_id"
              cols="12" sm="6" md="4" lg="3"
            >
              <MovieCard 
                :movie="movie" 
                @click="goToMovie(movie.id || movie.film_id)"
              />
            </v-col>
          </v-row>
        </v-window-item>

        <v-window-item value="actors">
          <div v-if="results.actors?.length === 0" class="text-center py-8">
            <v-icon size="96" class="mb-4">mdi-account-off</v-icon>
            <h3 class="mb-2">Актёры не найдены</h3>
            <p class="text-grey">Попробуйте изменить запрос поиска</p>
          </div>

          <v-row v-else>
            <v-col
              v-for="actor in results.actors"
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

        <v-window-item value="users">
          <div v-if="results.users?.length === 0" class="text-center py-8">
            <v-icon size="96" class="mb-4">mdi-account-group-off</v-icon>
            <h3 class="mb-2">Пользователи не найдены</h3>
            <p class="text-grey">Попробуйте изменить запрос поиска</p>
          </div>

          <v-list v-else class="users-list">
            <v-list-item
              v-for="user in results.users"
              :key="user.id"
              class="mb-2"
            >
              <template v-slot:prepend>
                <v-avatar color="primary" size="48">
                  <span class="text-h6">{{ getUserInitials(user.username) }}</span>
                </v-avatar>
              </template>
              <v-list-item-title>{{ user.username }}</v-list-item-title>
              <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
        </v-window-item>
      </v-window>

      <div v-if="hasNoResults" class="text-center py-12">
        <v-icon size="128" class="mb-4">mdi-magnify-remove</v-icon>
        <h2 class="mb-4">Ничего не найдено</h2>
        <p class="text-grey mb-6">Попробуйте другой запрос или проверьте правильность написания</p>
        <v-btn color="primary" @click="resetSearch">
          <v-icon start>mdi-refresh</v-icon>
          Сбросить поиск
        </v-btn>
      </div>
    </div>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieCard from '@/components/MovieCard.vue'
import ActorCard from '@/components/ActorCard.vue'
import { useSearchService } from '@/services/search.service'

const router = useRouter()
const route = useRoute()

const searchService = useSearchService()

const searchQuery = ref('')
const loading = ref(false)
const activeTab = ref('films')
const results = ref({
  films: [],
  actors: [],
  users: []
})

const totalResults = computed(() => {
  return (
    (results.value.films?.length || 0) +
    (results.value.actors?.length || 0) +
    (results.value.users?.length || 0)
  )
})

const hasNoResults = computed(() => {
  return (
    !loading.value &&
    searchQuery.value &&
    results.value.films?.length === 0 &&
    results.value.actors?.length === 0 &&
    results.value.users?.length === 0
  )
})

const performSearch = async () => {
  if (!searchQuery.value.trim()) {
    results.value = { films: [], actors: [], users: [] }
    return
  }

  try {
    loading.value = true
    const searchResults = await searchService.search(searchQuery.value)
    results.value = searchResults.results || { films: [], actors: [], users: [] }
  } catch (err) {
    console.error('Ошибка поиска:', err)
    results.value = { films: [], actors: [], users: [] }
  } finally {
    loading.value = false
  }
}

const getUserInitials = (username) => {
  if (!username) return 'U'
  const parts = username.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return username[0].toUpperCase()
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

const goToActor = (actorId) => {
  router.push(`/actor/${actorId}`)
}

const resetSearch = () => {
  searchQuery.value = ''
  results.value = { films: [], actors: [], users: [] }
}

// Загрузка при изменении query параметра
watch(() => route.query.q, (newQuery) => {
  if (newQuery && newQuery !== searchQuery.value) {
    searchQuery.value = newQuery
    performSearch()
  }
})

onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q
    performSearch()
  }
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

.users-list {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 16px;
}

:deep(.v-list-item-title) {
  color: white;
  font-weight: 500;
}

:deep(.v-list-item-subtitle) {
  color: #bdbdbd;
}

:deep(.v-tab) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.v-tab--selected) {
  color: white;
}
</style>