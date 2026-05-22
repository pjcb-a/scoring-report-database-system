import { defineStore } from 'pinia'

import {

  computed,

  ref

} from 'vue'

import {

  fetchEvents,

  createEvent,

  updateEvent,

  deleteEvent

} from '../services/eventService'

import {

  useEventContextStore

} from './eventContextStore'


export const useEventStore = defineStore(

  'eventStore',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const events = ref([])

    const loading = ref(false)

    const saving = ref(false)

    const error = ref(null)

    /*
    --------------------------------------------------------------------------
    GETTERS
    --------------------------------------------------------------------------
    */

    const totalEvents =
      computed(() => {

        return Array.isArray(events.value)

          ? events.value.length

          : 0
      })

    const activeEvents =
      computed(() => {

        if (!Array.isArray(events.value)) {
          return 0
        }

        return events.value.filter(

          event =>
            event.status === 'Ongoing'
            || event.status === 'Active'

        ).length
      })

    /*
    --------------------------------------------------------------------------
    NORMALIZE EVENTS
    --------------------------------------------------------------------------
    */

    const normalizeEvents =
      (payload) => {

        if (Array.isArray(payload)) {
          return payload
        }

        return []
      }

    /*
    --------------------------------------------------------------------------
    LOAD EVENTS
    --------------------------------------------------------------------------
    */

    const loadEvents =
      async () => {

        loading.value = true

        error.value = null

        try {

          const response =
            await fetchEvents()

          /*
          --------------------------------------------------------------------
          NORMALIZED RESPONSE
          --------------------------------------------------------------------
          */

          const payload =
            response?.data?.data

          events.value =
            normalizeEvents(payload)

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to load events.'

          /*
          --------------------------------------------------------------------
          FAIL SAFE
          --------------------------------------------------------------------
          */

          events.value = []

        } finally {

          loading.value = false
        }
      }

    /*
    --------------------------------------------------------------------------
    CREATE EVENT
    --------------------------------------------------------------------------
    */

    const createEventAction =
      async (payload) => {

        /*
        ----------------------------------------------------------------------
        PREVENT DUPLICATE SUBMITS
        ----------------------------------------------------------------------
        */

        if (saving.value) {
          return
        }

        saving.value = true

        error.value = null

        try {

          const response =
            await createEvent(payload)

          /*
          --------------------------------------------------------------------
          NORMALIZED RESPONSE
          --------------------------------------------------------------------
          */

          const newEvent =
            response?.data?.data

          /*
          --------------------------------------------------------------------
          ENSURE ARRAY STATE
          --------------------------------------------------------------------
          */

          if (!Array.isArray(events.value)) {

            events.value = []
          }

          /*
          --------------------------------------------------------------------
          APPEND EVENT
          --------------------------------------------------------------------
          */

          if (newEvent) {

            events.value.push(newEvent)
          }

          return newEvent

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to create event.'

          throw err

        } finally {

          saving.value = false
        }
      }

    /*
    --------------------------------------------------------------------------
    UPDATE EVENT
    --------------------------------------------------------------------------
    */

    const editEvent =
      async (

        eventId,

        payload

      ) => {

        loading.value = true

        error.value = null

        try {

          const response =
            await updateEvent(
              eventId,
              payload
            )

          const updatedEvent =
            response?.data?.data

          await loadEvents()

          const eventContextStore =
            useEventContextStore()

          const refreshedEvent =
            events.value.find(
              item =>
                Number(item.event_id)
                === Number(eventId)
            )
            || updatedEvent

          eventContextStore.syncCurrentEvent(
            refreshedEvent
          )

          return refreshedEvent || updatedEvent

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to update event.'

          throw err

        } finally {

          loading.value = false
        }
      }

    /*
    --------------------------------------------------------------------------
    DELETE EVENT
    --------------------------------------------------------------------------
    */

    const removeEvent =
      async (eventId) => {

        loading.value = true

        error.value = null

        try {

          await deleteEvent(eventId)

          /*
          --------------------------------------------------------------------
          ENSURE ARRAY STATE
          --------------------------------------------------------------------
          */

          if (!Array.isArray(events.value)) {

            events.value = []

            return
          }

          events.value =
            events.value.filter(

              event =>
                event.event_id !== eventId
            )

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to delete event.'

        } finally {

          loading.value = false
        }
      }

    return {

      /*
      ------------------------------------------------------------------------
      STATE
      ------------------------------------------------------------------------
      */

      events,

      loading,

      saving,

      error,

      /*
      ------------------------------------------------------------------------
      GETTERS
      ------------------------------------------------------------------------
      */

      totalEvents,

      activeEvents,

      /*
      ------------------------------------------------------------------------
      ACTIONS
      ------------------------------------------------------------------------
      */

      loadEvents,

      createEvent:
        createEventAction,

      editEvent,

      removeEvent
    }
  }
)