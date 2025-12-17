<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
      v-bind="{ ...props, ...$attrs }"
      class="movie-card movie-card-item"
      :elevation="isHovering ? 8 : 2"
      @click="$emit('click')"
    >
      <div class="poster-container">
        <div class="poster-wrapper">
          <img 
            :src="movie.poster_url" 
            :alt="movie.title"
            class="poster-image"
          />
          <div class="rating-badge" v-if="showRating">
            <v-icon small color="amber" class="mr-1">mdi-star</v-icon>
            <span>{{ displayRating }}</span>
          </div>
        </div>
      </div>
      
      <div class="movie-title">
        {{ movie.title }}
      </div>
    </v-card>
  </v-hover>
</template>

<script setup>
import { computed } from 'vue'
import { defineOptions } from 'vue'

const props = defineProps({
  movie: {
    type: Object,
    required: true
  }
})

const displayRating = computed(() => {
  const rating = props.movie.rating || props.movie.avg_rating
  return rating ? rating.toFixed(1) : '—'
})

const showRating = computed(() => {
  const rating = props.movie.rating || props.movie.avg_rating
  return rating !== null && rating !== undefined
})

defineEmits(['click'])

defineOptions({
  inheritAttrs: false
})
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  overflow: hidden;
  width: 150px; /* Фиксированная ширина */
  height: 280px; /* Фиксированная высота (150 * 1.5 + 44) */
  display: flex;
  flex-direction: column;
  background: #1e1e1e;
}

.movie-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.poster-container {
  position: relative;
  flex: 0 0 auto;
  width: 100%;
  height: 225px; /* 150 * 1.5 */
  overflow: hidden;
}

.poster-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Важно! */
  display: block;
  transition: transform 0.3s ease;
}

.movie-card:hover .poster-image {
  transform: scale(1.05);
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  z-index: 2;
  backdrop-filter: blur(2px);
}

.movie-title {
  flex: 1 1 auto;
  padding: 12px 8px;
  font-weight: 500;
  font-size: 0.9rem;
  line-height: 1.2;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  color: white;
  background: #1e1e1e;
}
</style>