import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (
      error.response?.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')

        const res = await axios.post(
          'http://127.0.0.1:8000/api/jwt/refresh',
          {},
          {
            headers: {
              Authorization: `Bearer ${refreshToken}`
            }
          }
        )

        localStorage.setItem('access_token', res.data.access_token)

        originalRequest.headers.Authorization =
          `Bearer ${res.data.access_token}`

        return api(originalRequest)
      } catch (e) {
        localStorage.clear()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)
