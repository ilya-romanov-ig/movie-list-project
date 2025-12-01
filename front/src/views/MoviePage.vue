<template>
  <PageWrapper>
    <!-- Поиск -->
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
        ></v-text-field>
      </v-col>
    </v-row>

    <!-- Основная информация о фильме -->
    <v-row class="mb-8">
      <!-- Постер фильма -->
      <v-col cols="12" md="4" lg="3">
        <v-img
          :src="movie.poster"
          aspect-ratio="2/3"
          class="movie-poster elevation-6"
          rounded
        >
          <template v-slot:placeholder>
            <v-row class="fill-height ma-0" align="center" justify="center">
              <v-progress-circular indeterminate color="grey lighten-5"></v-progress-circular>
            </v-row>
          </template>
        </v-img>
      </v-col>

      <!-- Информация о фильме -->
      <v-col cols="12" md="8" lg="9">
        <!-- Название и год -->
        <div class="d-flex align-center mb-2">
          <h1 class="movie-title">{{ movie.title }}</h1>
          <span class="movie-year ml-4">({{ movie.year }})</span>
        </div>

        <!-- Жанры -->
        <div class="mb-4">
          <v-chip
            v-for="genre in movie.genres"
            :key="genre.id"
            class="mr-2 mb-2"
            color="primary"
            @click="goToGenre(genre)"
          >
            {{ genre.name }}
          </v-chip>
        </div>

        <!-- Длительность и рейтинг -->
        <div class="d-flex align-center mb-4">
          <v-icon class="mr-2">mdi-clock-outline</v-icon>
          <span class="mr-4">{{ formatDuration(movie.duration) }}</span>
          
          <v-icon class="mr-2 ml-4" color="amber">mdi-star</v-icon>
          <span class="movie-rating">{{ movie.rating.toFixed(1) }}</span>
          <span class="ml-2 text-grey">({{ movie.ratingsCount }} оценок)</span>
        </div>

        <!-- Статистика -->
        <v-row class="mb-6">
          <v-col cols="6" md="4" lg="3">
            <div class="stat-item">
              <div class="stat-value">{{ movie.viewsCount.toLocaleString() }}</div>
              <div class="stat-label">Просмотров</div>
            </div>
          </v-col>
          <v-col cols="6" md="4" lg="3">
            <div class="stat-item">
              <div class="stat-value">{{ movie.favoritesCount.toLocaleString() }}</div>
              <div class="stat-label">В избранном</div>
            </div>
          </v-col>
        </v-row>

        <!-- Кнопки действий -->
        <div class="mb-6">
          <v-row>
            <v-col cols="12" sm="6" md="4" lg="3" v-for="action in actionButtons" :key="action.text">
              <v-btn
                :color="action.color"
                block
                :prepend-icon="action.icon"
                @click="handleAction(action.type)"
                variant="outlined"
              >
                {{ action.text }}
              </v-btn>
            </v-col>
          </v-row>
        </div>

        <!-- Описание -->
        <div class="mb-8">
          <h3 class="mb-2">Описание</h3>
          <p class="movie-description">{{ movie.description }}</p>
        </div>
      </v-col>
    </v-row>

    <!-- Актеры -->
    <div class="mb-8">
      <h2 class="mb-4">Актёры</h2>
      <v-slide-group show-arrows>
        <v-slide-item v-for="actor in movie.actors" :key="actor.id">
          <ActorCard 
            :actor="actor" 
            class="mx-3"
            @click="goToActor(actor)"
          />
        </v-slide-item>
      </v-slide-group>
    </div>

    <!-- Похожие фильмы -->
    <div v-if="similarMovies.length > 0">
      <h2 class="mb-4">Похожие фильмы</h2>
      <v-slide-group show-arrows>
        <v-slide-item v-for="similarMovie in similarMovies" :key="similarMovie.id">
          <MovieCard 
            :movie="similarMovie" 
            class="mx-3"
            @click="goToMovie(similarMovie.id)"
          />
        </v-slide-item>
      </v-slide-group>
    </div>
  </PageWrapper>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageWrapper from '@/components/PageWrapper.vue'
import MovieCard from '@/components/MovieCard.vue'
import ActorCard from '@/components/ActorCard.vue'

const router = useRouter()
const route = useRoute()
const searchQuery = ref('')

// Состояния пользователя
const isInFavorites = ref(false)
const isWatched = ref(false)
const userRating = ref(null)

// Данные фильма
const movie = ref({
  id: 1,
  title: 'Интерстеллар',
  year: 2014,
  duration: 169, // в минутах
  poster: 'https://via.placeholder.com/300x450',
  rating: 8.6,
  ratingsCount: 1500000,
  viewsCount: 5000000,
  favoritesCount: 1200000,
  description: 'Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.',
  genres: [
    { id: 1, name: 'Фантастика' },
    { id: 2, name: 'Драма' },
    { id: 3, name: 'Приключения' }
  ],
  actors: [
    { id: 1, name: 'Мэттью Макконахи', photo: 'https://via.placeholder.com/150x225', role: 'Купер' },
    { id: 2, name: 'Энн Хэтэуэй', photo: 'https://via.placeholder.com/150x225', role: 'Амелия Брэнд' },
    { id: 3, name: 'Джессика Честейн', photo: 'https.placeholder.com/150x225', role: 'Мёрф' },
    { id: 4, name: 'Майкл Кейн', photo: 'https://via.placeholder.com/150x225', role: 'Профессор Брэнд' }
  ]
})

// Похожие фильмы
const similarMovies = ref([
  { id: 2, title: 'Начало', poster: 'https://via.placeholder.com/150x225', rating: 8.8 },
  { id: 3, title: 'Дюна', poster: 'https://via.placeholder.com/150x225', rating: 8.0 },
  { id: 4, title: 'Марсианин', poster: 'https://via.placeholder.com/150x225', rating: 8.0 },
  { id: 5, title: 'Гравитация', poster: 'https://via.placeholder.com/150x225', rating: 7.7 },
  { id: 6, title: 'Прибытие', poster: 'https://via.placeholder.com/150x225', rating: 7.9 }
])

// Кнопки действий (динамические в зависимости от состояния)
const actionButtons = computed(() => {
  const baseButtons = [
    {
      text: isInFavorites.value ? 'Удалить из избранного' : 'Добавить в избранное',
      icon: isInFavorites.value ? 'mdi-heart' : 'mdi-heart-outline',
      color: isInFavorites.value ? 'error' : 'primary',
      type: 'favorite'
    },
    {
      text: isWatched.value ? 'Удалить из просмотренного' : 'Отметить как просмотренное',
      icon: isWatched.value ? 'mdi-eye-off' : 'mdi-eye',
      color: isWatched.value ? 'grey' : 'success',
      type: 'watched'
    }
  ]

  if (userRating.value) {
    baseButtons.push(
      {
        text: 'Изменить оценку',
        icon: 'mdi-star-edit',
        color: 'amber',
        type: 'rate'
      },
      {
        text: 'Удалить оценку',
        icon: 'mdi-star-remove',
        color: 'error',
        type: 'removeRating'
      }
    )
  } else {
    baseButtons.push({
      text: 'Оценить фильм',
      icon: 'mdi-star-plus',
      color: 'amber',
      type: 'rate'
    })
  }

  return baseButtons
})

// Функции
const formatDuration = (minutes) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return `${hours}ч ${mins}м`
}

const goToGenre = (genre) => {
  router.push({
    path: '/movies',
    query: { genre: genre.id }
  })
}

const goToActor = (actor) => {
  router.push(`/actor/${actor.id}`)
}

const goToMovie = (movieId) => {
  router.push(`/movie/${movieId}`)
}

const handleAction = (type) => {
  switch (type) {
    case 'favorite':
      isInFavorites.value = !isInFavorites.value
      // Здесь API вызов для добавления/удаления из избранного
      break
    case 'watched':
      isWatched.value = !isWatched.value
      // Здесь API вызов для отметки просмотра
      break
    case 'rate':
      // Открыть диалог оценки
      openRatingDialog()
      break
    case 'removeRating':
      userRating.value = null
      // Здесь API вызов для удаления оценки
      break
  }
}

const openRatingDialog = () => {
  // Реализация диалога оценки
  const rating = prompt('Оцените фильм от 1 до 10:')
  if (rating && rating >= 1 && rating <= 10) {
    userRating.value = parseFloat(rating)
    // Здесь API вызов для сохранения оценки
  }
}

// Загрузка данных фильма
onMounted(() => {
  const movieId = route.params.id
  // Здесь загрузка данных фильма по ID
  // fetchMovieData(movieId)
})
</script>

<style scoped>
.movie-poster {
  max-width: 300px;
  margin: 0 auto;
}

.movie-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
}

.movie-year {
  font-size: 1.5rem;
  color: #bdbdbd;
}

.movie-rating {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffd700;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #bdbdbd;
}

.movie-description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #e0e0e0;
  max-width: 800px;
}

h2, h3 {
  color: white;
  font-weight: 500;
}

:deep(.v-slide-group__content) {
  gap: 16px;
  padding: 8px 4px;
}
</style>