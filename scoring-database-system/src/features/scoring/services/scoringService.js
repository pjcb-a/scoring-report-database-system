import api from '@/services/api'

/*
|--------------------------------------------------------------------------
| GET SCORES BY EVENT
|--------------------------------------------------------------------------
*/

export const getScoresByEvent =
  async (eventId) => {

    const response =
      await api.get(

        `/events/${eventId}/scores`
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| CREATE SCORE
|--------------------------------------------------------------------------
*/

export const createScoreService =
  async (payload) => {

    const response =
      await api.post(

        '/scores',

        payload
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| FINALIZE GAME
|--------------------------------------------------------------------------
*/

export const finalizeGameService =
  async (gameId, payload) => {

    const response =
      await api.post(

        `/games/${gameId}/finalize`,

        payload
      )

    return response.data
}