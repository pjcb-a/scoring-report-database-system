import { computed, ref } from 'vue'

import {

  fetchGames,

  createGame,

  updateGame,

  deleteGame,

  fetchEventSports

} from '../services/gameService'


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const games = ref([])

const eventSports = ref([])

const loading = ref(false)

const error = ref(null)


/*
|--------------------------------------------------------------------------
| GETTERS
|--------------------------------------------------------------------------
*/

const totalGames = computed(() => {
  return games.value.length
})

const activeGames = computed(() => {

  return games.value.filter(
    game => game.status === 'Ongoing'
  ).length
})


/*
|--------------------------------------------------------------------------
| ACTIONS
|--------------------------------------------------------------------------
*/

const loadGames = async () => {

  loading.value = true

  error.value = null

  try {

    games.value =
      await fetchGames()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to load games.'

  } finally {

    loading.value = false
  }
}


const loadEventSports = async () => {

  try {

    eventSports.value =
      await fetchEventSports()

  } catch (err) {

    console.error(err)
  }
}


const addGame = async (
  payload
) => {

  try {

    await createGame(payload)

    await loadGames()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to create game.'
  }
}


const editGame = async (
  gameId,
  payload
) => {

  try {

    await updateGame(
      gameId,
      payload
    )

    await loadGames()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to update game.'
  }
}


const removeGame = async (
  gameId
) => {

  try {

    await deleteGame(gameId)

    await loadGames()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to delete game.'
  }
}


/*
|--------------------------------------------------------------------------
| STORE EXPORT
|--------------------------------------------------------------------------
*/

export function useGameStore() {

  return {

    games,

    eventSports,

    loading,

    error,

    totalGames,

    activeGames,

    loadGames,

    loadEventSports,

    addGame,

    editGame,

    removeGame
  }
}