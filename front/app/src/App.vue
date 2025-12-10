<template>
  <v-app>
    <Navbar />
    <v-main>
      <ErrorDisplay
        v-if="globalError"
        :error="globalError"
        title="Глобальная ошибка"
        :dismissible="true"
        @dismiss="clearGlobalError"
      />
      
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import Navbar from './components/Navbar.vue'
import ErrorDisplay from './components/ErrorDisplay.vue'

const globalError = ref(null)

const clearGlobalError = () => {
  globalError.value = null
}

// Перехватываем глобальные ошибки компонентов
onErrorCaptured((err, instance, info) => {
  console.error('Перехвачена ошибка компонента:', err)
  globalError.value = err
  // Возвращаем false чтобы предотвратить дальнейшее распространение
  return false
})
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>