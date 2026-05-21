import axios from 'axios'

import {

  useToastStore

} from '@/stores/toastStore'


/*
|--------------------------------------------------------------------------
| CENTRALIZED AXIOS INSTANCE
|--------------------------------------------------------------------------
|
| Single API layer for the entire application.
|
| Responsibilities:
| - request handling
| - response normalization
| - error handling
| - timeout management
| - interceptor architecture
|
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
| Future-ready:
| - auth tokens
| - request tracing
| - logging
|
*/

api.interceptors.request.use(

  config => {

    /*
    ------------------------------------------------------------------------
    FUTURE AUTH SUPPORT
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
| - backend errors
| - validation errors
| - network errors
| - timeout handling
| - toast notifications
|
*/

api.interceptors.response.use(

  response => {

    /*
    ------------------------------------------------------------------------
    NORMALIZED SUCCESS RESPONSE
    ------------------------------------------------------------------------
    */

    return response.data
  },

  error => {

    const toastStore =
      useToastStore()

    /*
    ------------------------------------------------------------------------
    SERVER RESPONSE ERROR
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
      BAD REQUEST
      ----------------------------------------------------------------------
      */

      if (status === 400) {

        toastStore.showToast(

          message,

          'warning'
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
      INTERNAL SERVER ERROR
      ----------------------------------------------------------------------
      */

      else if (status >= 500) {

        toastStore.showToast(

          'Internal server error.',

          'error'
        )
      }

      /*
      ----------------------------------------------------------------------
      GENERIC API ERROR
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
    NETWORK FAILURE
    ------------------------------------------------------------------------
    */

    else if (error.request) {

      toastStore.showToast(

        'Unable to connect to server.',

        'error'
      )
    }

    /*
    ------------------------------------------------------------------------
    UNKNOWN FAILURE
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