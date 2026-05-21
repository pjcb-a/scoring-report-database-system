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

import { runAsync } from '@/utils/request'


export const useGameStore = defineStore(

  'gameStore',

  () => {

    const games = ref([])

    const loading = ref(false)

    const error = ref(null)

    const eventContextStore =
      useEventContextStore()

    const loadGames = async () => {

      if (
        !eventContextStore.currentEventId
      ) {
        return
      }

      await runAsync(
        { loading, error },
        async () => {

          const response =
            await getGamesByEvent(

              eventContextStore.currentEventId
            )

          games.value =
            response.data || []
        }
      )
    }

    const addGame =
      async (payload) => {

        if (
          !eventContextStore.currentEventId
        ) {
          return
        }

        await runAsync(
          { loading, error },
          async () => {

            await createGame(

              eventContextStore.currentEventId,

              payload
            )

            await loadGames()
          },
          {
            showSuccessToast: true,
            successMessage: 'Game created successfully.'
          }
        )
      }

    const editGame =
      async (
        gameId,
        payload
      ) => {

        await runAsync(
          { loading, error },
          async () => {

            await updateGame(
              gameId,
              payload
            )

            await loadGames()
          },
          {
            showSuccessToast: true,
            successMessage: 'Game updated successfully.'
          }
        )
      }

    const removeGame =
      async (gameId) => {

        await runAsync(
          { loading, error },
          async () => {

            await deleteGame(gameId)

            games.value =
              games.value.filter(

                game =>
                  game.game_id !== gameId
              )
          },
          {
            showSuccessToast: true,
            successMessage: 'Game deleted successfully.'
          }
        )
      }

    return {

      games,

      loading,

      error,

      loadGames,

      addGame,

      editGame,

      removeGame
    }
  }
)
