<template>
  <v-app-bar color="green-darken-3" elevation="2">
    <!-- Кликабельное название сайта -->
    <router-link to="/" class="text-decoration-none d-flex align-center">
      <v-app-bar-title class="text-white font-weight-bold">
        Мой Сайт
      </v-app-bar-title>
    </router-link>

    <v-spacer></v-spacer>

    <!-- Меню пользователя -->
    <div v-if="isAuthenticated">
      <v-menu location="bottom end">
        <template v-slot:activator="{ props }">
          <v-btn
            icon
            v-bind="props"
            class="text-white"
            aria-label="Меню пользователя"
          >
            <v-icon size="large">mdi-account-circle</v-icon>
          </v-btn>
        </template>

        <v-list density="compact" min-width="150">
          <v-list-item
            prepend-icon="mdi-logout"
            value="logout"
            @click="logout"
            color="error"
          >
            <v-list-item-title>Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </div>

    <!-- Кнопки для неавторизованных пользователей -->
    <div v-else class="mr-2">
      <v-btn
        variant="text"
        color="white"
        :to="{ name: 'login' }"
        class="mx-1"
      >
        Войти
      </v-btn>
      <v-btn
        variant="outlined"
        color="white"
        :to="{ name: 'register' }"
        class="mx-1"
      >
        Регистрация
      </v-btn>
    </div>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('authToken')
})

const logout = () => {
  localStorage.removeItem('authToken')
  router.push('/login')
}
</script>

<style scoped>
.text-decoration-none {
  text-decoration: none;
}
</style>