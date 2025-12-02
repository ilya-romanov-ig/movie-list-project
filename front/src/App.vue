<template>
  <v-app>
    <Navbar />
    <v-main>
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </v-main>
  </v-app>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import Navbar from './components/Navbar.vue'

    const router = useRouter()
    const isAuthenticated = ref(false)

    onMounted(() => {
    isAuthenticated.value = !!localStorage.getItem('authToken')
    
    if (!isAuthenticated.value && window.location.pathname === '/') {
        router.push('/login')
    }
    })
</script>

<style>
/* Анимация перехода страниц */
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