import { createApp } from 'vue'

export default {
  install(app) {
    // Глобальный обработчик ошибок
    app.config.errorHandler = (err, vm, info) => {
      console.error('Vue ошибка:', err)
      console.error('Компонент:', vm)
      console.error('Информация:', info)
      
      // Можно отправить ошибку на сервер
      // sendErrorToServer(err, { component: vm, info })
    }

    // Глобальный обработчик неперехваченных промисов
    window.addEventListener('unhandledrejection', (event) => {
      console.error('Необработанная ошибка промиса:', event.reason)
      event.preventDefault()
    })

    // Глобальный обработчик ошибок сети
    window.addEventListener('error', (event) => {
      console.error('Глобальная ошибка:', event.error)
    })

    // Добавляем глобальный метод для показа ошибок
    app.config.globalProperties.$showError = (message, title = 'Ошибка') => {
      // Можно интегрировать с Vuetify Snackbar или другим UI компонентом
      console.error(`${title}: ${message}`)
    }
  }
}