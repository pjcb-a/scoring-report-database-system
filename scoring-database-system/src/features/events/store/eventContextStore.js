import { defineStore } from 'pinia'

import { ref, computed } from 'vue'


export const useEventContextStore = defineStore(

  'eventContext',

  () => {

    /*
    --------------------------------------------------
    STATE
    --------------------------------------------------
    */

    const currentEvent = ref(null)

    /*
    --------------------------------------------------
    GETTERS
    --------------------------------------------------
    */

    const hasSelectedEvent = computed(() => {

      return currentEvent.value !== null
    })

    const currentEventId = computed(() => {

      return currentEvent.value?.event_id || null
    })

    const currentEventName = computed(() => {

      return currentEvent.value?.event_name
        || 'Sports Reporting Database System'
    })

    /*
    --------------------------------------------------
    ACTIONS
    --------------------------------------------------
    */

    const setCurrentEvent = (event) => {

      currentEvent.value = event

      localStorage.setItem(
        'currentEvent',
        JSON.stringify(event)
      )
    }

    const clearCurrentEvent = () => {

      currentEvent.value = null

      localStorage.removeItem(
        'currentEvent'
      )
    }

    const loadStoredEvent = () => {

      const storedEvent = localStorage.getItem(
        'currentEvent'
      )

      if (storedEvent) {

        currentEvent.value =
          JSON.parse(storedEvent)
      }
    }

    return {

      /*
      STATE
      */

      currentEvent,

      /*
      GETTERS
      */

      hasSelectedEvent,

      currentEventId,

      currentEventName,

      /*
      ACTIONS
      */

      setCurrentEvent,

      clearCurrentEvent,

      loadStoredEvent
    }
  }
)