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
          @keyup.enter="performSearch"
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

    <div v-else>
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
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieSection from '@/components/MovieSection.vue'
import { useHomeService } from '@/services/home.service'
import { useSearchService } from '@/services/search.service'

const router = useRouter()
const homeService = useHomeService()
const searchService = useSearchService()

const searchQuery = ref('')
const searchMode = ref('фильмам')
const loading = ref(false)
const homeData = ref({
  top_films: { items: [] },
  newest_films: { items: [] },
  recommended: { items: [] },
  trending: { items: [] }
})

const searchModes = [
  { title: 'фильмам', value: 'фильмам' },
  { title: 'актерам', value: 'актерам' },
  { title: 'пользователям', value: 'пользователям' }
]

const hasMovies = computed(() => {
  return (
    homeData.value.top_films?.items?.length > 0 ||
    homeData.value.newest_films?.items?.length > 0 ||
    homeData.value.recommended?.items?.length > 0 ||
    homeData.value.trending?.items?.length > 0
  )
})

const loadHomeData = async () => {
  try {
    loading.value = true
    const data = await homeService.getHomeData()
    
    homeData.value = {
      top_films: data.top_films || { items: [] },
      newest_films: data.newest_films || { items: [] },
      recommended: data.recommended || { items: [] },
      trending: data.trending || { items: [] }
    }
  } catch (error) {
    console.error('Ошибка загрузки главной страницы:', error)
  } finally {
    loading.value = false
  }
}

const performSearch = async () => {
  if (!searchQuery.value.trim()) return

  try {
    loading.value = true
    const results = await searchService.search(searchQuery.value)
    
    // В зависимости от режима поиска показываем разные результаты
    if (searchMode.value === 'фильмам') {
      homeData.value = {
        top_films: { items: results.results.films || [] },
        newest_films: { items: [] },
        recommended: { items: [] },
        trending: { items: [] }
      }
    } else if (searchMode.value === 'актерам') {
      // TODO: Реализовать отображение актёров
      console.log('Результаты поиска актёров:', results.results.actors)
    }
  } catch (error) {
    console.error('Ошибка поиска:', error)
  } finally {
    loading.value = false
  }
}

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
</style>