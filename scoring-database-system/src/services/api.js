import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  response => response,
  error => {
    const message =
      error.response?.data?.message ||
      error.message ||
      'Request failed.'

    return Promise.reject(new Error(message))
  }
)

export const unwrapData = (response) => {
  return response.data?.data ?? response.data
}

export default api
