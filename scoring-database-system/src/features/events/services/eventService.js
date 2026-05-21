import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL EVENTS
|--------------------------------------------------------------------------
*/

export const fetchEvents = async () => {

  return await api.get(
    '/events'
  )
}


/*
|--------------------------------------------------------------------------
| GET SINGLE EVENT
|--------------------------------------------------------------------------
*/

export const fetchEvent = async (
  eventId
) => {

  return await api.get(
    `/events/${eventId}`
  )
}


/*
|--------------------------------------------------------------------------
| CREATE EVENT
|--------------------------------------------------------------------------
*/

export const createEvent = async (
  payload
) => {

  return await api.post(
    '/events',
    payload
  )
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

  return await api.put(

    `/events/${eventId}`,

    payload
  )
}


/*
|--------------------------------------------------------------------------
| DELETE EVENT
|--------------------------------------------------------------------------
*/

export const deleteEvent = async (
  eventId
) => {

  return await api.delete(
    `/events/${eventId}`
  )
}