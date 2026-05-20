import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET SCORE COMPONENTS
|--------------------------------------------------------------------------
*/

export const fetchJudgeScores = async () => {

  const response = await api.get(
    '/score-components'
  )

  return unwrapData(response)
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

  return unwrapData(response)
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

  return unwrapData(response)
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

  return unwrapData(response)
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

  return unwrapData(response)
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

  return unwrapData(response)
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

  return unwrapData(response)
}
