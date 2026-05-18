import api from '@/services/api'


/*
|--------------------------------------------------------------------------
| GET ALL GAMES
|--------------------------------------------------------------------------
*/

export const fetchGames = async () => {

  const response = await api.get(
    '/games'
  )

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
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

  return response.data
}