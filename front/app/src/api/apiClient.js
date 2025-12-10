export default class APIClient {
  constructor(config) {
    this.baseURL = config.baseURL || 'https://api.example.com'
    this.getToken = config.getToken
    this.onError = config.onError || console.error
  }

  async request(endpoint, options = {}) {
    const token = await this.getToken?.()
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    }
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    try {
      const url = endpoint.startsWith('http') ? endpoint : `${this.baseURL}${endpoint}`
      const response = await fetch(url, {
        ...options,
        headers,
      })

      // Обработка HTTP ошибок
      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response)
        const error = new Error(errorData.message || `HTTP ${response.status}`)
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
      if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
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
      return { message: `HTTP ${response.status}: ${response.statusText}` }
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
    return this.request(url, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put(endpoint, data = {}, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    return this.request(url, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async patch(endpoint, data = {}, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    return this.request(url, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  async delete(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString()
    const url = query ? `${endpoint}?${query}` : endpoint
    return this.request(url, { method: 'DELETE' })
  }
}