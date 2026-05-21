import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET SCORING TYPES
|--------------------------------------------------------------------------
*/

export const getScoringTypes =
  async () => {

    const response = await api.get(
      '/scoring-types'
    )

    return response.data
  }

/*
|--------------------------------------------------------------------------
| GET EVENT SPORTS
|--------------------------------------------------------------------------
*/

export const getSportsByEvent =
  async (eventId) => {

    const response = await api.get(

      `/events/${eventId}/sports`
    )

    return response.data
}

/*
|--------------------------------------------------------------------------
| ADD SPORT TO EVENT
|--------------------------------------------------------------------------
*/

export const addSportToEvent =
  async (eventId, payload) => {

    const response = await api.post(

      `/events/${eventId}/sports`,

      payload
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| DELETE EVENT SPORT
|--------------------------------------------------------------------------
*/

export const removeEventSport =
  async (eventSportId) => {

    const response = await api.delete(

      `/event-sports/${eventSportId}`
    )

    return response.data
}