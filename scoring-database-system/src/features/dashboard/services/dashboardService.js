import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| FETCH EVENT DASHBOARD
|--------------------------------------------------------------------------
*/

export const fetchDashboardSummaryByEvent =
  async (eventId) => {

    return await api.get(

      `/events/${eventId}/dashboard`
    )
}


/*
|--------------------------------------------------------------------------
| FETCH EVENT RANKINGS
|--------------------------------------------------------------------------
*/

export const fetchEventRankings =
  async (eventId) => {

    return await api.get(

      `/events/${eventId}/reports/rankings`
    )
}