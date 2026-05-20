import api, { unwrapData } from '@/services/api'


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

    events: unwrapData(events),

    sports: unwrapData(sports),

    games: unwrapData(games),

    scores: unwrapData(scores)
  }
}
