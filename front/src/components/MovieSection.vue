<template>
  <div class="my-6">
    <h2>{{ title }}</h2>
    <v-slide-group show-arrows>
      <v-slide-group-item v-for="(movie, index) in movies" :key="movie.id || movie.film_id || index">
        <MovieCard 
          :movie="movie" 
          class="movie-card-item" 
          @click="handleMovieClick(movie)"
        />
      </v-slide-group-item>
    </v-slide-group>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import MovieCard from './MovieCard.vue'

const router = useRouter()

defineProps({
  title: String,
  movies: Array
})

const handleMovieClick = (movie) => {
  const movieId = movie.id || movie.film_id
  if (movieId) {
    router.push(`/movie/${movieId}`)
  }
}
</script>

<style scoped>
h2 {
  font-weight: 500;
  margin-bottom: 16px;
  font-size: 1.5rem;
  color: white;
}

.movie-card-item {
  margin: 0 16px !important;
}

:deep(.v-slide-group__content) {
  gap: 16px;
  padding: 8px 4px;
}
</style>