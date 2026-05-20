import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL SPORTS
|--------------------------------------------------------------------------
*/

export const fetchSports = async () => {

  const response = await api.get(
    '/sports'
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| CREATE SPORT
|--------------------------------------------------------------------------
*/

export const createSport = async (
  payload
) => {

  const response = await api.post(
    '/sports',
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| UPDATE SPORT
|--------------------------------------------------------------------------
*/

export const updateSport = async (
  sportId,
  payload
) => {

  const response = await api.put(
    `/sports/${sportId}`,
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| DELETE SPORT
|--------------------------------------------------------------------------
*/

export const deleteSport = async (
  sportId
) => {

  const response = await api.delete(
    `/sports/${sportId}`
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| GET SCORING TYPES
|--------------------------------------------------------------------------
*/

export const fetchScoringTypes = async () => {

  const response = await api.get(
    '/scoring-types'
  )

  return unwrapData(response)
}
