<template>
  <v-hover v-slot="{ isHovering, props }">
    <v-card
      v-bind="props"
      class="movie-card"
      :elevation="isHovering ? 8 : 2"
      @click="$emit('click')"
    >
      <div class="poster-container">
        <v-img 
          :src="movie.poster" 
          aspect-ratio="2/3"
        >
          <div class="rating-badge" v-if="movie.rating">
            <v-icon small color="amber" class="mr-1">mdi-star</v-icon>
            <span>{{ movie.rating }}</span>
          </div>
        </v-img>
      </div>
      
      <v-card-text class="pa-3 text-center movie-title">
        {{ movie.title }}
      </v-card-text>
    </v-card>
  </v-hover>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  movie: {
    type: Object,
    required: true,
    default: () => ({
      id: null,
      title: '',
      poster: '',
      rating: null
    })
  }
})

defineEmits(['click'])
</script>

<style scoped>
.movie-card {
  cursor: pointer;
  transition: all 0.3s ease;
  max-width: 200px;
  border-radius: 8px;
  overflow: hidden;
}

.movie-card:hover {
  transform: translateY(-4px);
}

.poster-container {
  position: relative;
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.movie-title {
  font-weight: 500;
  font-size: 0.9rem;
  line-height: 1.2;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>