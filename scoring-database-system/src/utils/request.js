import { isRef } from 'vue'
import { useToastStore } from '@/features/events/store/toastStore'

/**
 * Standardized async request lifecycle manager.
 * Automates loading/error states, centralizes logging, and shows optional toast alerts.
 *
 * @param {Object} state - Object containing loading/error ref variables: { loading, error }
 * @param {Function} callback - The async function containing the operation
 * @param {Object} options - Custom execution options
 * @param {boolean} options.showSuccessToast - Set true to show a success toast on completion
 * @param {string} options.successMessage - Custom success message
 * @param {boolean} options.showErrorToast - Set true if you want runAsync to explicitly trigger an error toast (normally handled globally by api.js interceptors)
 */
export async function runAsync(state, callback, options = {}) {
  const {
    showSuccessToast = false,
    successMessage = 'Action completed successfully.',
    showErrorToast = false
  } = options

  const loading = state?.loading
  const error = state?.error

  if (loading && isRef(loading)) {
    loading.value = true
  }
  if (error && isRef(error)) {
    error.value = null
  }

  try {
    const result = await callback()

    if (showSuccessToast) {
      try {
        const toastStore = useToastStore()
        toastStore.showToast(successMessage, 'success')
      } catch (e) {
        console.error('[runAsync] Failed to show success toast:', e)
      }
    }

    return result
  } catch (err) {
    // If the request was cancelled, do not set state errors or trigger toasts
    if (err && (err.name === 'CanceledError' || err.__CANCEL__ || err.message === 'canceled')) {
      throw err
    }

    const errorMsg = err.message || 'An unexpected error occurred.'
    if (error && isRef(error)) {
      error.value = errorMsg
    }

    if (showErrorToast) {
      try {
        const toastStore = useToastStore()
        toastStore.showToast(errorMsg, 'error')
      } catch (e) {
        console.error('[runAsync] Failed to show error toast:', e)
      }
    }

    // Always log full error trace for debugging, eliminating scattered console.error in stores
    console.error('[runAsync] Async operation failed:', err)
    throw err
  } finally {
    if (loading && isRef(loading)) {
      loading.value = false
    }
  }
}
