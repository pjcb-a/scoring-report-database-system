import api from '@/services/api'

/*
|--------------------------------------------------------------------------
| GET JUDGES BY EVENT
|--------------------------------------------------------------------------
*/

export const getJudgesByEvent =
  async (eventId) => {

    const response =
      await api.get(

        `/events/${eventId}/judges`
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| CREATE JUDGE
|--------------------------------------------------------------------------
*/

export const createJudge =
  async (eventId, payload) => {

    const response =
      await api.post(

        `/events/${eventId}/judges`,

        payload
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| DELETE JUDGE
|--------------------------------------------------------------------------
*/

export const deleteJudge =
  async (judgeId) => {

    const response =
      await api.delete(

        `/judges/${judgeId}`
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| GET JUDGE SCORES BY EVENT
|--------------------------------------------------------------------------
*/

export const getJudgeScoresByEvent =
  async (eventId) => {

    const response =
      await api.get(

        `/events/${eventId}/judge-scores`
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| CREATE JUDGE SCORE
|--------------------------------------------------------------------------
*/

export const createJudgeScoreService =
  async (payload) => {

    const response =
      await api.post(

        '/judge-scores',

        payload
      )

    return response.data
}

/*
|--------------------------------------------------------------------------
| FINALIZE JUDGE GAME
|--------------------------------------------------------------------------
*/

export const finalizeJudgeGameService =
  async (gameId, payload) => {

    const response =
      await api.post(

        `/judge-games/${gameId}/finalize`,

        payload
      )

    return response.data
}