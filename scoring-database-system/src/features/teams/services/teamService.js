import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL TEAMS
|--------------------------------------------------------------------------
*/

export const fetchTeams = async () => {

  const response = await api.get(
    '/teams'
  )

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
}