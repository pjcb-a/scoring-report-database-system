import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET GAMES OF EVENT
|--------------------------------------------------------------------------
*/

export const getGamesByEvent =
  async (eventId, options = {}) => {

    const params = {}

    if (options.scheduledOnly) {
      params.scheduled_only = true
    }

    const response = await api.get(

      `/events/${eventId}/games`,

      { params }
    )

    return response.data
}

export const getScheduledGamesByEvent =
  async (eventId) =>
    getGamesByEvent(eventId, { scheduledOnly: true })


/*
|--------------------------------------------------------------------------
| GET SINGLE GAME
|--------------------------------------------------------------------------
*/

export const getGame =
  async (gameId) => {

    const response = await api.get(

      `/games/${gameId}`
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| CREATE GAME INSIDE EVENT
|--------------------------------------------------------------------------
*/

export const createGame =
  async (eventId, payload) => {

    const response = await api.post(

      `/events/${eventId}/games`,

      payload
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| UPDATE GAME
|--------------------------------------------------------------------------
*/

export const updateGame =
  async (gameId, payload) => {

    const response = await api.put(

      `/games/${gameId}`,

      payload
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| DELETE GAME
|--------------------------------------------------------------------------
*/

export const deleteGame =
  async (gameId) => {

    const response = await api.delete(

      `/games/${gameId}`
    )

    return response.data
}
