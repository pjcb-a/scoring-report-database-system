import axios from '@/services/axios'


/*
|--------------------------------------------------------------------------
| FETCH EVENT DASHBOARD
|--------------------------------------------------------------------------
*/

export const fetchDashboardSummaryByEvent =
  async (eventId) => {

    return await axios.get(

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

    return await axios.get(

      `/events/${eventId}/reports/rankings`
    )
}