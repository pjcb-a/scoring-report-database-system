import axios from 'axios'
import { useToastStore } from '@/features/events/store/toastStore'

// Keep track of active requests to enable cancellation
const pendingRequests = new Map()

// Retry configurations
const MAX_RETRIES = 2
const RETRY_DELAY_MS = 1000

/**
 * Generates a unique key for an API request based on method, URL, and payload/parameters.
 */
function getRequestKey(config) {
  const { method, url, params, data } = config
  const dataStr = typeof data === 'string' ? data : JSON.stringify(data)
  return [method, url, JSON.stringify(params), dataStr].join('&')
}

/**
 * Adds a request to the tracker. Cancels identical active requests to prevent double-clicks.
 */
function addPendingRequest(config) {
  const key = getRequestKey(config)

  // Cancel duplicate if config permits (defaults to true)
  if (config.cancelDuplicate !== false && pendingRequests.has(key)) {
    const { abort } = pendingRequests.get(key)
    abort('Duplicate request cancelled (double-click prevention).')
    pendingRequests.delete(key)
  }

  const controller = new AbortController()
  config.signal = config.signal || controller.signal

  pendingRequests.set(key, {
    abort: (reason) => controller.abort(reason),
    cancelOnNav: config.cancelOnNav !== false
  })
}

/**
 * Removes a request from the tracker when it resolves or fails.
 */
function removePendingRequest(config) {
  const key = getRequestKey(config)
  pendingRequests.delete(key)
}

/**
 * Aborts all active requests scheduled for cancellation on route navigation.
 */
export function cancelAllPendingRequests(reason = 'Navigation cancelled') {
  pendingRequests.forEach((item, key) => {
    if (item.cancelOnNav) {
      item.abort(reason)
      pendingRequests.delete(key)
    }
  })
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

/*
|--------------------------------------------------------------------------
| REQUEST INTERCEPTOR
|--------------------------------------------------------------------------
*/
api.interceptors.request.use(
  (config) => {
    addPendingRequest(config)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/*
|--------------------------------------------------------------------------
| RESPONSE INTERCEPTOR & GLOBAL ERROR HANDLER
|--------------------------------------------------------------------------
*/
api.interceptors.response.use(
  (response) => {
    if (response.config) {
      removePendingRequest(response.config)
    }
    return response
  },
  async (error) => {
    const config = error.config

    // If the request was cancelled, reject silently without toasts or retries
    if (axios.isCancel(error)) {
      return Promise.reject(error)
    }

    if (config) {
      removePendingRequest(config)

      // Auto-retry GET requests on network drops or 5xx server errors
      const isGet = config.method?.toLowerCase() === 'get'
      const isTransient = !error.response || error.response.status >= 500
      config._retryCount = config._retryCount || 0

      if (isGet && isTransient && config._retryCount < MAX_RETRIES) {
        config._retryCount++
        console.warn(`[API] Retrying GET request ${config.url} (${config._retryCount}/${MAX_RETRIES})...`)
        await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY_MS))
        return api(config)
      }
    }

    let message = 'An unexpected error occurred.'
    let errors = null

    if (error.response) {
      // Server responded with a status code outside the 2xx range
      const responseData = error.response.data
      message = responseData?.message || `Request failed with status ${error.response.status}`
      errors = responseData?.errors || null

      // Format custom validation failures if returned by the backend
      if (errors && typeof errors === 'object') {
        const errorList = Object.entries(errors)
          .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(', ') : val}`)
          .join('; ')
        if (errorList) {
          message = `${message} (${errorList})`
        }
      }
    } else if (error.request) {
      // Request was made but no response was received (e.g. server offline)
      message = 'Cannot connect to the server. Please ensure the backend is running.'
    } else {
      // Error setting up the request
      message = error.message
    }

    // Trigger centralized Toast notification automatically
    try {
      const toastStore = useToastStore()
      toastStore.showToast(message, 'error')
    } catch (e) {
      console.error('[API] Failed to show error toast:', e)
    }

    // Construct a standardized high-fidelity Error object
    const customError = new Error(message)
    customError.status = error.response?.status
    customError.errors = errors
    customError.originalError = error

    return Promise.reject(customError)
  }
)

export const unwrapData = (response) => {
  return response.data?.data ?? response.data
}

export default api


