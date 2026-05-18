import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| DASHBOARD SUMMARY
|--------------------------------------------------------------------------
*/

export const fetchDashboardSummary = async () => {

  const [

    events,

    sports,

    games,

    scores

  ] = await Promise.all([

    api.get('/events'),

    api.get('/sports'),

    api.get('/games'),

    api.get('/game-scores')
  ])

  return {

    events: events.data,

    sports: sports.data,

    games: games.data,

    scores: scores.data
  }
}