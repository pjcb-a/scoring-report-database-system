import { computed, ref } from 'vue'

import {

  fetchEvents,

  createEvent,

  updateEvent,

  deleteEvent

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

const loadEvents = async () => {

  loading.value = true

  error.value = null

  try {

    events.value = await fetchEvents()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to load events.'

  } finally {

    loading.value = false
  }
}


const addEvent = async (
  payload
) => {

  try {

    await createEvent(payload)

    await loadEvents()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to create event.'
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

    await loadEvents()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to update event.'
  }
}


const removeEvent = async (
  eventId
) => {

  try {

    await deleteEvent(eventId)

    await loadEvents()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to delete event.'
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
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    events,
    loading,
    error,

    /*
    --------------------------------------------------------------------------
    GETTERS
    --------------------------------------------------------------------------
    */

    totalEvents,
    activeEvents,

    /*
    --------------------------------------------------------------------------
    ACTIONS
    --------------------------------------------------------------------------
    */

    loadEvents,
    addEvent,
    editEvent,
    removeEvent
  }
}