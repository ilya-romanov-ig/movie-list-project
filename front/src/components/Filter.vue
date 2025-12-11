<template>
  <v-card class="filters-card" elevation="2">
    <v-card-title class="d-flex justify-space-between align-center">
      <span>Фильтры</span>
      <v-btn
        v-if="showReset"
        icon
        size="small"
        @click="resetFilters"
        variant="text"
      >
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </v-card-title>
    
    <v-card-text>
      <v-select
        v-model="localFilters.genre"
        :items="genres"
        item-title="name"
        item-value="genre_id"
        label="Жанр"
        clearable
        class="mb-4"
        @update:model-value="emitFilters"
      />

      <v-select
        v-model="localFilters.year"
        :items="years"
        label="Год выпуска"
        clearable
        class="mb-4"
        @update:model-value="emitFilters"
      />

      <v-select
        v-model="localFilters.actor"
        :items="actors"
        item-title="name"
        item-value="actor_id"
        label="Актёр"
        clearable
        class="mb-4"
        @update:model-value="emitFilters"
      />

      <v-select
        v-model="localFilters.sortBy"
        :items="sortOptions"
        label="Сортировка"
        class="mb-4"
        @update:model-value="emitFilters"
      />

      <div class="mb-4">
        <div class="d-flex justify-space-between mb-2">
          <span class="text-caption text-grey">Рейтинг</span>
          <span class="text-caption text-grey">{{ ratingRangeText }}</span>
        </div>
        <v-range-slider
          v-model="localFilters.ratingRange"
          :min="0"
          :max="10"
          :step="0.5"
          thumb-label
          hide-details
          @update:model-value="emitFilters"
        />
      </div>

      <v-btn
        color="primary"
        block
        @click="applyFilters"
        class="mb-2"
      >
        Применить
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useGenreService } from '@/services/genre.service'
import { useActorService } from '@/services/actor.service'

const props = defineProps({
  filters: {
    type: Object,
    default: () => ({
      genre: null,
      year: null,
      actor: null,
      sortBy: 'rating_desc',
      ratingRange: [0, 10]
    })
  },
  showReset: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:filters', 'apply', 'reset'])

const genreService = useGenreService()
const actorService = useActorService()

const localFilters = ref({ ...props.filters })
const genres = ref([])
const actors = ref([])
const years = ref([])

const sortOptions = [
  { title: 'По рейтингу (убыв.)', value: 'rating_desc' },
  { title: 'По рейтингу (возр.)', value: 'rating_asc' },
  { title: 'По году (новые)', value: 'year_desc' },
  { title: 'По году (старые)', value: 'year_asc' },
  { title: 'По названию (А-Я)', value: 'title_asc' },
  { title: 'По названию (Я-А)', value: 'title_desc' },
]

const ratingRangeText = computed(() => {
  const [min, max] = localFilters.value.ratingRange
  if (min === 0 && max === 10) return 'Любой'
  if (min === 0) return `до ${max}`
  if (max === 10) return `от ${min}`
  return `${min} - ${max}`
})

const loadGenres = async () => {
  try {
    const genresData = await genreService.getGenres({ limit: 100 })
    genres.value = genresData.items || []
  } catch (err) {
    console.error('Ошибка загрузки жанров:', err)
  }
}

const loadActors = async () => {
  try {
    const actorsData = await actorService.getActors({ limit: 50 })
    actors.value = actorsData.items || []
  } catch (err) {
    console.error('Ошибка загрузки актёров:', err)
  }
}

const generateYears = () => {
  const currentYear = new Date().getFullYear()
  for (let year = currentYear; year >= 1900; year--) {
    years.value.push(year)
  }
}

const applyFilters = () => {
  emit('apply', localFilters.value)
}

const resetFilters = () => {
  localFilters.value = {
    genre: null,
    year: null,
    actor: null,
    sortBy: 'rating_desc',
    ratingRange: [0, 10]
  }
  emit('reset')
  emit('update:filters', localFilters.value)
}

const emitFilters = () => {
  emit('update:filters', localFilters.value)
}

// Реакция на изменения props
watch(() => props.filters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })

onMounted(() => {
  loadGenres()
  loadActors()
  generateYears()
})
</script>

<style scoped>
.filters-card {
  background-color: #1e1e1e;
  position: sticky;
  top: 20px;
}

:deep(.v-card-title) {
  color: white;
  font-weight: 500;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7);
}

:deep(.v-field__input) {
  color: white;
}

:deep(.v-range-slider__track-background) {
  background-color: rgba(255, 255, 255, 0.2);
}

:deep(.v-range-slider__track-fill) {
  background-color: #4CAF50;
}

:deep(.v-select__selection-text) {
  color: white;
}
</style>