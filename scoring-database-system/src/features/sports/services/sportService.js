import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL SPORTS
|--------------------------------------------------------------------------
*/

export const fetchSports = async () => {

  const response = await api.get(
    '/sports'
  )

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
}