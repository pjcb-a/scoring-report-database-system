import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET SCORE COMPONENTS
|--------------------------------------------------------------------------
*/

export const fetchJudgeScores = async () => {

  const response = await api.get(
    '/score-components'
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| CREATE SCORE COMPONENT
|--------------------------------------------------------------------------
*/

export const createJudgeScore = async (
  payload
) => {

  const response = await api.post(
    '/score-components',
    payload
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| UPDATE SCORE COMPONENT
|--------------------------------------------------------------------------
*/

export const updateJudgeScore = async (
  scoreComponentId,
  payload
) => {

  const response = await api.put(
    `/score-components/${scoreComponentId}`,
    payload
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| DELETE SCORE COMPONENT
|--------------------------------------------------------------------------
*/

export const deleteJudgeScore = async (
  scoreComponentId
) => {

  const response = await api.delete(
    `/score-components/${scoreComponentId}`
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| GET GAME SCORES
|--------------------------------------------------------------------------
*/

export const fetchGameScores = async () => {

  const response = await api.get(
    '/game-scores'
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| GET CRITERIA
|--------------------------------------------------------------------------
*/

export const fetchCriteria = async () => {

  const response = await api.get(
    '/criteria'
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| GET JUDGES
|--------------------------------------------------------------------------
*/

export const fetchJudges = async () => {

  const response = await api.get(
    '/judges'
  )

  return response.data
}