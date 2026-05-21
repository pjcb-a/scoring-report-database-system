import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET TEAMS OF EVENT
|--------------------------------------------------------------------------
*/

export const getTeamsByEvent =
  async (eventId) => {

    const response = await api.get(

      `/events/${eventId}/teams`
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| GET SINGLE TEAM
|--------------------------------------------------------------------------
*/

export const getTeam =
  async (teamId) => {

    const response = await api.get(

      `/teams/${teamId}`
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| CREATE TEAM INSIDE EVENT
|--------------------------------------------------------------------------
*/

export const createTeam =
  async (eventId, payload) => {

    const response = await api.post(

      `/events/${eventId}/teams`,

      payload
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| UPDATE TEAM
|--------------------------------------------------------------------------
*/

export const updateTeam =
  async (teamId, payload) => {

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

export const deleteTeam =
  async (teamId) => {

    const response = await api.delete(

      `/teams/${teamId}`
    )

    return response.data
}
