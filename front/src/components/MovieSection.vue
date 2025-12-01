<template>
  <div class="my-6">
    <h2>{{ title }}</h2>
    <v-slide-group show-arrows>
      <v-slide-item v-for="(movie, index) in movies" :key="index">
        <MovieCard 
          :movie="movie" 
          class="movie-card-item" 
          @click="handleMovieClick(movie)"
        />
      </v-slide-item>
    </v-slide-group>
  </div>
</template>

<script setup>
import MovieCard from './MovieCard.vue'

defineProps({
  title: String,
  movies: Array
})

const handleMovieClick = (movie) => {
  console.log('Клик по фильму:', movie)
  // Здесь можно добавить навигацию на страницу фильма
  // Например: router.push(`/movie/${movie.id}`)
}
</script>

<style scoped>
h2 {
  font-weight: 500;
  margin-bottom: 16px;
  font-size: 1.5rem;
}

.movie-card-item {
  margin: 0 16px !important;
}

:deep(.v-slide-group__content) {
  gap: 16px;
  padding: 8px 4px;
}
</style>