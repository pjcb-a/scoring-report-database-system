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

    const error = ref(null)

    /*
    --------------------------------------------------------------------------
    GETTERS
    --------------------------------------------------------------------------
    */

    const totalEvents =
      computed(() => {

        return events.value.length
      })

    const activeEvents =
      computed(() => {

        return events.value.filter(

          event =>
            event.status === 'Active'

        ).length
      })

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

          events.value =
            response.data || []

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to load events.'

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

        loading.value = true

        error.value = null

        try {

          const response =
            await createEvent(payload)

          /*
          --------------------------------------------------------------------
          APPEND NEW EVENT
          --------------------------------------------------------------------
          */

          if (response.data) {

            events.value.push(
              response.data
            )
          }

          return response

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to create event.'

          throw err

        } finally {

          loading.value = false
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

          await updateEvent(

            eventId,

            payload
          )

          await loadEvents()

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to update event.'

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