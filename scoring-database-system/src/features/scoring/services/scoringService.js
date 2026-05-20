import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL SCORES
|--------------------------------------------------------------------------
*/

export const fetchScores = async () => {

  const response = await api.get(
    '/game-scores'
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| CREATE SCORE
|--------------------------------------------------------------------------
*/

export const createScore = async (
  payload
) => {

  const response = await api.post(
    '/game-scores',
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| UPDATE SCORE
|--------------------------------------------------------------------------
*/

export const updateScore = async (
  scoreId,
  payload
) => {

  const response = await api.put(
    `/game-scores/${scoreId}`,
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| DELETE SCORE
|--------------------------------------------------------------------------
*/

export const deleteScore = async (
  scoreId
) => {

  const response = await api.delete(
    `/game-scores/${scoreId}`
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| GET GAMES
|--------------------------------------------------------------------------
*/

export const fetchGames = async () => {

  const response = await api.get(
    '/games'
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| GET TEAMS
|--------------------------------------------------------------------------
*/

export const fetchTeams = async () => {

  const response = await api.get(
    '/teams'
  )

  return unwrapData(response)
}
