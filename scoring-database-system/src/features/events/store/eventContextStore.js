import { defineStore } from 'pinia'

import {

  ref,

  computed

} from 'vue'


export const useEventContextStore = defineStore(

  'eventContext',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const currentEvent = ref(null)

    /*
    --------------------------------------------------------------------------
    GETTERS
    --------------------------------------------------------------------------
    */

    const hasSelectedEvent =
      computed(() => {

        return currentEvent.value !== null
      })

    const currentEventId =
      computed(() => {

        return currentEvent.value?.event_id || null
      })

    const currentEventName =
      computed(() => {

        return currentEvent.value?.event_name

          ||

          'Sports Reporting Database System'
      })

    /*
    --------------------------------------------------------------------------
    SET CURRENT EVENT
    --------------------------------------------------------------------------
    */

    const setCurrentEvent =
      (event) => {

        currentEvent.value = event

        localStorage.setItem(

          'currentEvent',

          JSON.stringify(event)
        )
      }

    const syncCurrentEvent =
      (updatedEvent) => {

        if (!updatedEvent?.event_id) {
          return
        }

        if (
          Number(currentEvent.value?.event_id)
          !== Number(updatedEvent.event_id)
        ) {
          return
        }

        const mergedEvent = {
          ...currentEvent.value,
          ...updatedEvent
        }

        setCurrentEvent(mergedEvent)
      }

    /*
    --------------------------------------------------------------------------
    CLEAR CURRENT EVENT
    --------------------------------------------------------------------------
    */

    const clearCurrentEvent =
      () => {

        currentEvent.value = null

        localStorage.removeItem(
          'currentEvent'
        )
      }

    /*
    --------------------------------------------------------------------------
    LOAD STORED EVENT
    --------------------------------------------------------------------------
    */

    const loadStoredEvent =
      () => {

        try {

          const storedEvent =
            localStorage.getItem(
              'currentEvent'
            )

          if (storedEvent) {

            currentEvent.value =
              JSON.parse(storedEvent)
          }

        } catch (error) {

          console.error(error)

          currentEvent.value = null
        }
      }

    /*
    --------------------------------------------------------------------------
    INITIALIZE STORE
    --------------------------------------------------------------------------
    */

    loadStoredEvent()

    return {

      /*
      ------------------------------------------------------------------------
      STATE
      ------------------------------------------------------------------------
      */

      currentEvent,

      /*
      ------------------------------------------------------------------------
      GETTERS
      ------------------------------------------------------------------------
      */

      hasSelectedEvent,

      currentEventId,

      currentEventName,

      /*
      ------------------------------------------------------------------------
      ACTIONS
      ------------------------------------------------------------------------
      */

      setCurrentEvent,

      syncCurrentEvent,

      clearCurrentEvent,

      loadStoredEvent
    }
  }
)