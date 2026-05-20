import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL EVENTS
|--------------------------------------------------------------------------
*/

export const fetchEvents = async () => {

  const response = await api.get(
    '/events'
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| GET SINGLE EVENT
|--------------------------------------------------------------------------
*/

export const fetchEvent = async (
  eventId
) => {

  const response = await api.get(
    `/events/${eventId}`
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| CREATE EVENT
|--------------------------------------------------------------------------
*/

export const createEvent = async (
  payload
) => {

  const response = await api.post(
    '/events',
    payload
  )

  return unwrapData(response)
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

  const response = await api.put(
    `/events/${eventId}`,
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| DELETE EVENT
|--------------------------------------------------------------------------
*/

export const deleteEvent = async (
  eventId
) => {

  const response = await api.delete(
    `/events/${eventId}`
  )

  return unwrapData(response)
}
