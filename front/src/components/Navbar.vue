<template>
  <v-app-bar
    class="custom-navbar"
    elevation="4"
    height="70"
  >
    <!-- Пустое пространство слева для центрирования -->
    <v-spacer></v-spacer>

    <!-- Логотип по центру -->
    <router-link to="/" class="text-decoration-none d-flex align-center">
      <v-app-bar-title class="logo-title">
        <v-icon size="32" class="mr-2" color="white">mdi-movie</v-icon>
        <span class="logo-text">Filmoтека</span>
      </v-app-bar-title>
    </router-link>

    <v-spacer></v-spacer>

    <!-- Правая часть с кнопками пользователя -->
    <div class="nav-actions">
      <div v-if="isAuthenticated">
        <v-menu location="bottom end">
          <template v-slot:activator="{ props }">
            <v-btn
              icon
              v-bind="props"
              class="user-btn"
              size="large"
              aria-label="Меню пользователя"
            >
              <v-avatar size="40">
                <v-icon size="32" color="white">mdi-account-circle</v-icon>
              </v-avatar>
            </v-btn>
          </template>

          <v-list density="compact" min-width="200" class="user-menu">
            <v-list-item
              prepend-icon="mdi-home"
              value="home"
              @click="goToHome"
              class="mb-1"
            >
              <v-list-item-title>Главная</v-list-item-title>
            </v-list-item>
            <v-divider class="my-2"></v-divider>
            <v-list-item
              prepend-icon="mdi-account"
              value="profile"
              @click="goToProfile"
              class="mb-1"
            >
              <v-list-item-title>Профиль</v-list-item-title>
            </v-list-item>
            <v-list-item
              prepend-icon="mdi-bookmark"
              value="saved"
              @click="goToSaved"
              class="mb-1"
            >
              <v-list-item-title>Сохранённое</v-list-item-title>
            </v-list-item>
            <v-divider class="my-2"></v-divider>
            <v-list-item
              prepend-icon="mdi-logout"
              value="logout"
              @click="logout"
              class="logout-item"
            >
              <v-list-item-title>Выйти</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>

      <div v-else class="auth-buttons">
        <v-btn
          variant="text"
          color="white"
          :to="{ name: 'login' }"
          class="mx-1 auth-btn"
          prepend-icon="mdi-login"
        >
          Войти
        </v-btn>
        <v-btn
          variant="outlined"
          color="white"
          :to="{ name: 'register' }"
          class="mx-1 auth-btn"
          prepend-icon="mdi-account-plus"
        >
          Регистрация
        </v-btn>
      </div>
    </div>
  </v-app-bar>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const authStore = useAuthStore()
const { logout: authLogout } = useAuth()

const isAuthenticated = computed(() => authStore.isAuthenticated)

const goToHome = () => {
  router.push('/')
}

const goToProfile = () => {
  router.push('/profile')
}

const goToSaved = () => {
  router.push('/saved')
}

const logout = () => {
  authLogout()
  router.push('/')
}
</script>

<style scoped>
.custom-navbar {
  background: linear-gradient(135deg, #66ea85 20%, #5f06b9 80%) !important;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.logo-title {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.logo-text {
  font-family: 'Roboto', 'Segoe UI', sans-serif;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: 1px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  background:  #ffffff;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: all 0.3s ease;
}

.logo-text:hover {
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
  transform: scale(1.05);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-btn {
  transition: all 0.3s ease;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.711) !important;
  backdrop-filter: blur(10px);
}

.user-btn:hover {
  background: rgba(255, 255, 255, 0.2) !important;
  transform: scale(1.1);
}

.user-btn .v-icon {
  transition: all 0.3s ease;
}

.user-btn:hover .v-icon {
  transform: rotate(10deg);
}

.user-menu {
  border-radius: 12px !important;
  border: 1px solid rgba(102, 234, 133, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
  margin-top: 8px;
  backdrop-filter: blur(20px);
  background: rgb(255, 255, 255) !important;
}

.user-menu :deep(.v-list-item) {
  border-radius: 8px;
  margin: 4px;
  transition: all 0.2s ease;
}

.user-menu :deep(.v-list-item:hover) {
  background: rgba(102, 234, 133, 0.064) !important;
  transform: translateX(4px);
}

.user-menu :deep(.v-list-item__prepend) .v-icon {
  color: #1dee4eda;
}

.logout-item :deep(.v-list-item__prepend) .v-icon {
  color: #ff5252;
}

.auth-buttons {
  display: flex;
  gap: 8px;
}

.auth-btn {
  font-weight: 600;
  letter-spacing: 0.5px;
  border-radius: 25px !important;
  padding: 8px 20px !important;
  transition: all 0.3s ease !important;
  text-transform: none;
  backdrop-filter: blur(10px);
}

.auth-btn.v-btn--variant-text {
  background: rgba(255, 255, 255, 0.1) !important;
}

.auth-btn.v-btn--variant-outlined {
  border: 2px solid rgba(255, 255, 255, 0.5) !important;
}

.auth-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2) !important;
}

.auth-btn.v-btn--variant-text:hover {
  background: rgba(255, 255, 255, 0.2) !important;
}

.auth-btn.v-btn--variant-outlined:hover {
  border-color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
}

/* Адаптивность */
@media (max-width: 960px) {
  .logo-text {
    font-size: 1.5rem;
  }
  
  .auth-btn {
    padding: 6px 12px !important;
    font-size: 0.875rem;
  }
  
  .user-btn {
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 600px) {
  .logo-title {
    position: static;
    transform: none;
    margin-left: 16px;
  }
  
  .logo-text {
    font-size: 1.25rem;
  }
  
  .auth-buttons {
    flex-direction: column;
    gap: 4px;
  }
  
  .auth-btn {
    padding: 4px 8px !important;
    font-size: 0.75rem;
    min-width: auto;
  }
  
  .custom-navbar {
    height: 60px;
  }
}

/* Анимации */
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.custom-navbar {
  background-size: 200% 200% !important;
  animation: gradientShift 10s ease infinite;
}
</style>