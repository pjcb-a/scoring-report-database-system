import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL SCORES
|--------------------------------------------------------------------------
*/

export const fetchScores = async () => {

  const response = await api.get(
    '/game-scores'
  )

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
}