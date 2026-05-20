import api from '@/services/axios'


/*
|--------------------------------------------------------------------------
| FETCH EVENT DASHBOARD
|--------------------------------------------------------------------------
*/

export const fetchDashboardSummaryByEvent =
  async (eventId) => {

    const response = await api.get(

      `/events/${eventId}/dashboard`
    )

    return response.data
}


/*
|--------------------------------------------------------------------------
| FETCH EVENT RANKINGS
|--------------------------------------------------------------------------
*/

export const fetchEventRankings =
  async (eventId) => {

    const response = await api.get(

      `/events/${eventId}/reports/rankings`
    )

    return response.data
}