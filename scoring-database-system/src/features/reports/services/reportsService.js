import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET REPORT DATA
|--------------------------------------------------------------------------
*/

export const fetchReports = async () => {

  const response = await api.get(
    '/reports'
  )

  return unwrapData(response)
}

export const fetchParticipationReports = async () => {
  const response = await api.get('/reports/participation')

  return unwrapData(response)
}

export const fetchJudgingReports = async () => {
  const response = await api.get('/reports/judging-summary')

  return unwrapData(response)
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

  return unwrapData(response)
}
