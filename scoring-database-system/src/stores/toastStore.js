import { defineStore } from 'pinia'

import { ref } from 'vue'


export const useToastStore = defineStore(

  'toastStore',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const toasts = ref([])

    /*
    --------------------------------------------------------------------------
    SHOW TOAST
    --------------------------------------------------------------------------
    */

    const showToast = (

      message,

      type = 'success'

    ) => {

      const id = Date.now()

      toasts.value.push({

        id,

        message,

        type
      })

      /*
      ------------------------------------------------------------------------
      AUTO REMOVE
      ------------------------------------------------------------------------
      */

      setTimeout(() => {

        toasts.value =
          toasts.value.filter(

            toast => toast.id !== id
          )

      }, 3000)
    }

    return {

      toasts,

      showToast
    }
  }
)