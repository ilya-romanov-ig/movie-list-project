import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthService } from '@/services'
import { useAuthStore } from '@/stores/auth'

export function useAuth() {
  const router = useRouter()
  const authService = useAuthService()
  const authStore = useAuthStore()
  
  const loading = ref(false)
  const error = ref(null)
  
  const login = async (email, password, rememberMe = false) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await authService.login(email, password)
      
      // Сохраняем токен
      authStore.setToken(response.access_token)
      
      // TODO: Обработка rememberMe если нужно
      
      // Редирект на главную
      router.push('/')
    } catch (err) {
      error.value = err.message || 'Ошибка входа'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const register = async (username, email, password) => {
    try {
      loading.value = true
      error.value = null
      
      await authService.register(username, email, password)
      
      // После регистрации автоматически логинимся
      await login(email, password)
    } catch (err) {
      error.value = err.message || 'Ошибка регистрации'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const logout = () => {
    authService.logout()
    authStore.logout()
    router.push('/login')
  }
  
  return {
    loading,
    error,
    login,
    register,
    logout,
  }
}
