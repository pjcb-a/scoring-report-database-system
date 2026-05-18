import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET REPORT DATA
|--------------------------------------------------------------------------
*/

export const fetchReports = async () => {

  const response = await api.get(
    '/game-scores'
  )

  return response.data
}


/*
|--------------------------------------------------------------------------
| GET EVENTS
|--------------------------------------------------------------------------
*/

export const fetchEvents = async () => {

  const response = await api.get(
    '/events'
  )

  return response.data
}