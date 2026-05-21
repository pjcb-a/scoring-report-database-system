import axios from 'axios'

import {

  useToastStore

} from '@/stores/toastStore'


/*
|--------------------------------------------------------------------------
| AXIOS INSTANCE
|--------------------------------------------------------------------------
*/

const api = axios.create({

  baseURL:

    import.meta.env.VITE_API_BASE_URL

    ||

    'http://127.0.0.1:5000/api',

  timeout: 10000,

  headers: {

    'Content-Type': 'application/json'
  }
})


/*
|--------------------------------------------------------------------------
| REQUEST INTERCEPTOR
|--------------------------------------------------------------------------
|
| Future-ready for:
| - auth tokens
| - request metadata
| - logging
|
*/

api.interceptors.request.use(

  config => {

    /*
    ------------------------------------------------------------------------
    AUTH TOKEN PLACEHOLDER
    ------------------------------------------------------------------------
    */

    // const token = localStorage.getItem('token')

    // if (token) {
    //   config.headers.Authorization =
    //     `Bearer ${token}`
    // }

    return config
  },

  error => {

    return Promise.reject(error)
  }
)


/*
|--------------------------------------------------------------------------
| RESPONSE INTERCEPTOR
|--------------------------------------------------------------------------
|
| Centralized:
| - server errors
| - network failures
| - unauthorized access
| - toast notifications
|
*/

api.interceptors.response.use(

  response => {

    return response
  },

  error => {

    const toastStore =
      useToastStore()

    /*
    ------------------------------------------------------------------------
    SERVER RESPONSE ERRORS
    ------------------------------------------------------------------------
    */

    if (error.response) {

      const status =
        error.response.status

      const message =

        error.response.data?.message

        ||

        'Unexpected server error.'

      /*
      ----------------------------------------------------------------------
      UNAUTHORIZED
      ----------------------------------------------------------------------
      */

      if (status === 401) {

        toastStore.showToast(

          'Unauthorized access.',

          'error'
        )
      }

      /*
      ----------------------------------------------------------------------
      FORBIDDEN
      ----------------------------------------------------------------------
      */

      else if (status === 403) {

        toastStore.showToast(

          'Access forbidden.',

          'error'
        )
      }

      /*
      ----------------------------------------------------------------------
      NOT FOUND
      ----------------------------------------------------------------------
      */

      else if (status === 404) {

        toastStore.showToast(

          message,

          'error'
        )
      }

      /*
      ----------------------------------------------------------------------
      VALIDATION / BAD REQUEST
      ----------------------------------------------------------------------
      */

      else if (status === 400) {

        toastStore.showToast(

          message,

          'warning'
        )
      }

      /*
      ----------------------------------------------------------------------
      INTERNAL SERVER ERROR
      ----------------------------------------------------------------------
      */

      else {

        toastStore.showToast(

          message,

          'error'
        )
      }
    }

    /*
    ------------------------------------------------------------------------
    NETWORK / CONNECTION ERROR
    ------------------------------------------------------------------------
    */

    else if (error.request) {

      toastStore.showToast(

        'Unable to connect to the server.',

        'error'
      )
    }

    /*
    ------------------------------------------------------------------------
    UNKNOWN ERROR
    ------------------------------------------------------------------------
    */

    else {

      toastStore.showToast(

        'Something went wrong.',

        'error'
      )
    }

    return Promise.reject(error)
  }
)

export default api