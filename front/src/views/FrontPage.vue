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
        >
          <template #append>
            <v-select
              v-model="searchMode"
              :items="['фильмам', 'актерам', 'пользователям']"
              dense
              outlined
              hide-details
              color="white"
              class="mode-select"
              item-color="grey"
            ></v-select>
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <MovieSection title="Рекомендованное" :movies="recommendedMovies" />

    <MovieSection title="Высокий рейтинг" :movies="topRatedMovies" />

    <MovieSection title="Новинки" :movies="newMovies" />
  </PageWrapper>
</template>

<script setup>
import { ref } from 'vue'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieSection from '@/components/MovieSection.vue'

const searchQuery = ref('')
const searchMode = ref('фильмам')

const recommendedMovies = ref(Array.from({ length: 10 }, (_, i) => ({
  id: i + 1,
  title: `Фильм ${i + 1}`,
  poster: 'https://via.placeholder.com/150x225',
  rating: 8.5
})))

const topRatedMovies = ref(Array.from({ length: 10 }, (_, i) => ({
  id: i + 11,
  title: `Фильм ${i + 1}`,
  poster: 'https://via.placeholder.com/150x225',
  rating: 9.0
})))

const newMovies = ref(Array.from({ length: 10 }, (_, i) => ({
  id: i + 21,
  title: `Новинка ${i + 1}`,
  poster: 'https://via.placeholder.com/150x225',
  rating: 7.8
})))
</script>