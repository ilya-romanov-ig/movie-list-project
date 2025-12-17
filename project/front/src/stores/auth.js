import { defineStore } from "pinia"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: JSON.parse(localStorage.getItem("user") || 'null'),
    userId: localStorage.getItem("userId") || null,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
  },
  
  actions: {
    async setToken(token) {
      this.token = token
      localStorage.setItem("token", token)
      
      // Получаем информацию о пользователе после установки токена
      await this.fetchCurrentUser()
    },
    
    async fetchCurrentUser() {
      try {
        // Используем window.fetch напрямую, чтобы избежать circular dependency
        const response = await fetch('http://localhost:8001/auth/me', {
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }
        
        const userData = await response.json()
        this.user = userData
        this.userId = userData.id
        localStorage.setItem("user", JSON.stringify(userData))
        localStorage.setItem("userId", userData.id)
        
        return userData
      } catch (error) {
        console.error("Failed to fetch user data:", error)
        this.clearAuth()
        throw error
      }
    },
    
    setUser(user) {
      this.user = user
      this.userId = user.id
      localStorage.setItem("user", JSON.stringify(user))
      localStorage.setItem("userId", user.id)
    },
    
    clearAuth() {
      this.token = null
      this.user = null
      this.userId = null
      localStorage.removeItem("token")
      localStorage.removeItem("user")
      localStorage.removeItem("userId")
    },
    
    logout() {
      this.clearAuth()
    },
  },
})