export default class APIClient {
  constructor(config) {
    this.baseURL = config.baseURL || 'http://localhost:8001'
    this.getToken = config.getToken
    this.onError = config.onError || console.error
  }

  async request(endpoint, options = {}) {
    const token = await this.getToken?.()
    
    // Определяем, является ли data FormData
    const isFormData = options.body instanceof FormData
    
    // Формируем заголовки
    const headers = {
      ...options.headers,
    }
    
    // Добавляем Content-Type только если это не FormData
    if (!isFormData && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json'
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    try {
      const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`
      
      const response = await fetch(url, {
        ...options,
        headers,
        credentials: 'include',
      })

      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response)
        const error = new Error(errorData.detail || errorData.message || `HTTP ${response.status}`)
        error.status = response.status
        error.data = errorData
        throw error
      }

      // Парсим успешный ответ
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      } else {
        return await response.text()
      }
    } catch (error) {
      // Обработка сетевых ошибок
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        const networkError = new Error('Ошибка сети. Проверьте подключение к интернету.')
        networkError.isNetworkError = true
        this.onError(networkError)
        throw networkError
      }
      
      this.onError(error)
      throw error
    }
  }

  async parseErrorResponse(response) {
    try {
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        return await response.json()
      } else {
        return { message: await response.text() }
      }
    } catch {
      return { 
        message: `HTTP ${response.status}: ${response.statusText}`,
        detail: `HTTP ${response.status}: ${response.statusText}`
      }
    }
  }

  async get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    return this.request(url, { method: 'GET' })
  }

  async post(endpoint, data = {}, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    
    const isFormData = data instanceof FormData
    const body = isFormData ? data : JSON.stringify(data)
    
    return this.request(url, {
      method: 'POST',
      body,
    })
  }

  async put(endpoint, data = {}, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    
    const isFormData = data instanceof FormData
    const body = isFormData ? data : JSON.stringify(data)
    
    return this.request(url, {
      method: 'PUT',
      body,
    })
  }

  async patch(endpoint, data = {}, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    
    const isFormData = data instanceof FormData
    const body = isFormData ? data : JSON.stringify(data)
    
    return this.request(url, {
      method: 'PATCH',
      body,
    })
  }

  async delete(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    return this.request(url, { method: 'DELETE' })
  }
}