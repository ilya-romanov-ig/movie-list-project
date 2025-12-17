import { ref } from 'vue'

export function useErrorHandling() {
  const error = ref(null)
  const loading = ref(false)

  const executeWithErrorHandling = async (fn, errorMessage = 'Ошибка выполнения') => {
    try {
      error.value = null
      loading.value = true
      return await fn()
    } catch (err) {
      error.value = err
      console.error(`${errorMessage}:`, err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    error,
    loading,
    executeWithErrorHandling,
    clearError
  }
}