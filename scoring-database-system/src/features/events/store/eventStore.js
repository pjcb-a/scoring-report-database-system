import { computed, ref } from 'vue'

import {
  createEvent,
  deleteEvent,
  getEvents,
  updateEvent
} from '../services/eventService'

/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const events = ref([])

const loading = ref(false)

const error = ref(null)

/*
|--------------------------------------------------------------------------
| GETTERS
|--------------------------------------------------------------------------
*/

const totalEvents = computed(() => {
  return events.value.length
})

const activeEvents = computed(() => {

  return events.value.filter(
    event => event.status === 'Active'
  ).length
})

/*
|--------------------------------------------------------------------------
| ACTIONS
|--------------------------------------------------------------------------
*/

const fetchEvents = async () => {

  loading.value = true

  error.value = null

  try {

    events.value = await getEvents()

  } catch (err) {

    error.value =
      'Failed to load events.'

    console.error(err)

  } finally {

    loading.value = false
  }
}

const addEvent = async (payload) => {

  try {

    await createEvent(payload)

    await fetchEvents()

  } catch (err) {

    error.value =
      'Failed to create event.'

    console.error(err)
  }
}

const editEvent = async (
  eventId,
  payload
) => {

  try {

    await updateEvent(
      eventId,
      payload
    )

    await fetchEvents()

  } catch (err) {

    error.value =
      'Failed to update event.'

    console.error(err)
  }
}

const removeEvent = async (
  eventId
) => {

  try {

    await deleteEvent(eventId)

    await fetchEvents()

  } catch (err) {

    error.value =
      'Failed to delete event.'

    console.error(err)
  }
}

/*
|--------------------------------------------------------------------------
| STORE EXPORT
|--------------------------------------------------------------------------
*/

export function useEventStore() {

  return {

    /*
    |----------------------------------------------------------------------
    | STATE
    |----------------------------------------------------------------------
    */

    events,
    loading,
    error,

    /*
    |----------------------------------------------------------------------
    | GETTERS
    |----------------------------------------------------------------------
    */

    totalEvents,
    activeEvents,

    /*
    |----------------------------------------------------------------------
    | ACTIONS
    |----------------------------------------------------------------------
    */

    fetchEvents,
    addEvent,
    editEvent,
    removeEvent
  }
}