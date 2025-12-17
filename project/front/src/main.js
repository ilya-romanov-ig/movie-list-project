import { createApp } from "vue"
import App from "./App.vue"

import vuetify from "./plugins/vuetify"
import router from "./router"
import errorHandler from "./plugins/errorHandler"

import { createPinia } from "pinia"
import { useAuthStore } from "./stores/auth"

import APIClient from "./api/apiClient"
import { API_KEY } from "./api/useApi"

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

// Добавляем обработчик ошибок
app.use(errorHandler)

app.provide(
  API_KEY,
  new APIClient({
    baseURL: 'http://localhost:8001',
    getToken: async () => {
      const auth = useAuthStore()
      return auth.token
    },
    onError: (error) => {
      console.error("API ERROR:", error)
      // Можно показать уведомление пользователю
      app.config.globalProperties.$showError?.(
        error.message || 'Ошибка при выполнении запроса',
        'Ошибка API'
      )
    },
  })
)

app.use(router)
app.use(vuetify)

app.mount("#app")