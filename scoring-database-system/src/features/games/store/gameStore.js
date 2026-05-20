import { defineStore } from 'pinia'

import { ref } from 'vue'

import {

  getGamesByEvent,

  createGame,

  updateGame,

  deleteGame

} from '../services/gameService'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'


export const useGameStore = defineStore(

  'gameStore',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const games = ref([])

    const loading = ref(false)

    const error = ref(null)

    /*
    --------------------------------------------------------------------------
    EVENT CONTEXT
    --------------------------------------------------------------------------
    */

    const eventContextStore =
      useEventContextStore()

    /*
    --------------------------------------------------------------------------
    LOAD GAMES
    --------------------------------------------------------------------------
    */

    const loadGames = async () => {

      if (
        !eventContextStore.currentEventId
      ) {
        return
      }

      loading.value = true

      error.value = null

      try {

        const response =
          await getGamesByEvent(

            eventContextStore.currentEventId
          )

        games.value =
          response.data || []

      } catch (err) {

        console.error(err)

        error.value =
          err.message ||
          'Failed to load games.'

      } finally {

        loading.value = false
      }
    }

    /*
    --------------------------------------------------------------------------
    CREATE GAME
    --------------------------------------------------------------------------
    */

    const addGame =
      async (payload) => {

        try {

          await createGame(payload)

          await loadGames()

        } catch (err) {

          console.error(err)

          throw err
        }
      }

    /*
    --------------------------------------------------------------------------
    UPDATE GAME
    --------------------------------------------------------------------------
    */

    const editGame =
      async (
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

          throw err
        }
      }

    /*
    --------------------------------------------------------------------------
    DELETE GAME
    --------------------------------------------------------------------------
    */

    const removeGame =
      async (gameId) => {

        try {

          await deleteGame(gameId)

          games.value =
            games.value.filter(

              game =>
                game.game_id !== gameId
            )

        } catch (err) {

          console.error(err)

          throw err
        }
      }

    return {

      /*
      ------------------------------------------------------------------------
      STATE
      ------------------------------------------------------------------------
      */

      games,

      loading,

      error,

      /*
      ------------------------------------------------------------------------
      METHODS
      ------------------------------------------------------------------------
      */

      loadGames,

      addGame,

      editGame,

      removeGame
    }
  }
)