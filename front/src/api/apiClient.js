class APIClient {
  constructor({
    baseURL = "",
    getToken = null,
    onError = null,
    timeout = 10000,
  } = {}) {
    this.baseURL = baseURL;
    this.getToken = getToken;
    this.onError = onError;
    this.timeout = timeout;
  }

  withTimeout(promise) {
    return Promise.race([
      promise,
      new Promise((_, reject) =>
        setTimeout(() => reject({ message: "Request timeout" }), this.timeout)
      ),
    ]);
  }

  async parseError(response) {
    let data = null;
    try {
      data = await response.json();
    } catch {}

    return {
      status: response.status,
      data,
      message: data?.message || response.statusText || "Ошибка запроса",
    };
  }

  async request(method, url, body = null, config = {}) {
    const headers = {
      "Content-Type": "application/json",
      ...config.headers,
    };

    if (this.getToken) {
      const token = await this.getToken();
      if (token) headers.Authorization = `Bearer ${token}`;
    }

    const options = {
      method,
      headers,
      ...config,
    };

    if (body) {
      options.body = JSON.stringify(body);
    }

    const fetchPromise = fetch(this.baseURL + url, options);

    const response = await this.withTimeout(fetchPromise);

    if (!response.ok) {
      const error = await this.parseError(response);
      if (this.onError) this.onError(error);
      throw error;
    }

    if (response.status === 204) return {};

    return response.json();
  }

  get(url, params = {}, config = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request("GET", query ? `${url}?${query}` : url, null, config);
  }

  post(url, body = {}, config = {}) {
    return this.request("POST", url, body, config);
  }

  put(url, body = {}, config = {}) {
    return this.request("PUT", url, body, config);
  }

  patch(url, body = {}, config = {}) {
    return this.request("PATCH", url, body, config);
  }

  delete(url, config = {}) {
    return this.request("DELETE", url, null, config);
  }
}

export default APIClient;
