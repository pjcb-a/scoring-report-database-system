import api from '@/services/axios'


/*
|--------------------------------------------------------------------------
| GET EVENT RANKINGS
|--------------------------------------------------------------------------
*/

export const getEventRankings =
  async (eventId) => {

    const response = await api.get(

      `/events/${eventId}/reports/rankings`
    )

    return response.data
}