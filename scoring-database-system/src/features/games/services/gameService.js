import api from '@/services/axios'


/*
|--------------------------------------------------------------------------
| GET GAMES OF EVENT
|--------------------------------------------------------------------------
*/

export const getGamesByEvent =
  async (eventId) => {

    const response = await api.get(

      `/events/${eventId}/games`
    )

    return response.data
}


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
| CREATE GAME
|--------------------------------------------------------------------------
*/

export const createGame =
  async (payload) => {

    const response = await api.post(

      '/games',

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