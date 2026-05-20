import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL TEAMS
|--------------------------------------------------------------------------
*/

export const fetchTeams = async () => {

  const response = await api.get(
    '/teams'
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| CREATE TEAM
|--------------------------------------------------------------------------
*/

export const createTeam = async (
  payload
) => {

  const response = await api.post(
    '/teams',
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| UPDATE TEAM
|--------------------------------------------------------------------------
*/

export const updateTeam = async (
  teamId,
  payload
) => {

  const response = await api.put(
    `/teams/${teamId}`,
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| DELETE TEAM
|--------------------------------------------------------------------------
*/

export const deleteTeam = async (
  teamId
) => {

  const response = await api.delete(
    `/teams/${teamId}`
  )

  return unwrapData(response)
}
