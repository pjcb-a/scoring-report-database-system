import api, { unwrapData } from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL GAMES
|--------------------------------------------------------------------------
*/

export const fetchGames = async () => {

  const response = await api.get(
    '/games'
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| CREATE GAME
|--------------------------------------------------------------------------
*/

export const createGame = async (
  payload
) => {

  const response = await api.post(
    '/games',
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| UPDATE GAME
|--------------------------------------------------------------------------
*/

export const updateGame = async (
  gameId,
  payload
) => {

  const response = await api.put(
    `/games/${gameId}`,
    payload
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| DELETE GAME
|--------------------------------------------------------------------------
*/

export const deleteGame = async (
  gameId
) => {

  const response = await api.delete(
    `/games/${gameId}`
  )

  return unwrapData(response)
}


/*
|--------------------------------------------------------------------------
| GET EVENT SPORTS
|--------------------------------------------------------------------------
*/

export const fetchEventSports = async () => {

  const response = await api.get(
    '/event-sports'
  )

  return unwrapData(response)
}
