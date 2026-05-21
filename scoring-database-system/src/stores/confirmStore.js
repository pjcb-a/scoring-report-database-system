import { defineStore } from 'pinia'

import { ref } from 'vue'


export const useConfirmStore = defineStore(

  'confirmStore',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const isOpen = ref(false)

    const title = ref('')

    const message = ref('')

    const onConfirm = ref(null)

    /*
    --------------------------------------------------------------------------
    OPEN CONFIRM
    --------------------------------------------------------------------------
    */

    const openConfirm = (

      options

    ) => {

      title.value =
        options.title

      message.value =
        options.message

      onConfirm.value =
        options.onConfirm

      isOpen.value = true
    }

    /*
    --------------------------------------------------------------------------
    CLOSE CONFIRM
    --------------------------------------------------------------------------
    */

    const closeConfirm = () => {

      isOpen.value = false

      title.value = ''

      message.value = ''

      onConfirm.value = null
    }

    /*
    --------------------------------------------------------------------------
    CONFIRM ACTION
    --------------------------------------------------------------------------
    */

    const confirmAction =
      async () => {

        if (onConfirm.value) {

          await onConfirm.value()
        }

        closeConfirm()
      }

    return {

      isOpen,

      title,

      message,

      openConfirm,

      closeConfirm,

      confirmAction
    }
  }
)