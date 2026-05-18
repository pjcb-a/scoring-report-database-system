import api from '@/services/api'

/*
|--------------------------------------------------------------------------
| GET ALL EVENTS
|--------------------------------------------------------------------------
*/

export const getEvents = async () => {

  try {

    const response = await api.get('/events')

    return response.data

  } catch (error) {

    console.error(
      'Failed to fetch events:',
      error
    )

    throw error
  }
}

/*
|--------------------------------------------------------------------------
| GET SINGLE EVENT
|--------------------------------------------------------------------------
*/

export const getEventById = async (eventId) => {

  try {

    const response = await api.get(
      `/events/${eventId}`
    )

    return response.data

  } catch (error) {

    console.error(
      'Failed to fetch event:',
      error
    )

    throw error
  }
}

/*
|--------------------------------------------------------------------------
| CREATE EVENT
|--------------------------------------------------------------------------
*/

export const createEvent = async (payload) => {

  try {

    const response = await api.post(
      '/events',
      payload
    )

    return response.data

  } catch (error) {

    console.error(
      'Failed to create event:',
      error
    )

    throw error
  }
}

/*
|--------------------------------------------------------------------------
| UPDATE EVENT
|--------------------------------------------------------------------------
*/

export const updateEvent = async (
  eventId,
  payload
) => {

  try {

    const response = await api.put(
      `/events/${eventId}`,
      payload
    )

    return response.data

  } catch (error) {

    console.error(
      'Failed to update event:',
      error
    )

    throw error
  }
}

/*
|--------------------------------------------------------------------------
| DELETE EVENT
|--------------------------------------------------------------------------
*/

export const deleteEvent = async (
  eventId
) => {

  try {

    const response = await api.delete(
      `/events/${eventId}`
    )

    return response.data

  } catch (error) {

    console.error(
      'Failed to delete event:',
      error
    )

    throw error
  }
}