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