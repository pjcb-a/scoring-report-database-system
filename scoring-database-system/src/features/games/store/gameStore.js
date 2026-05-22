import { defineStore } from 'pinia'

import { ref } from 'vue'

import {

  getGamesByEvent,

  getScheduledGamesByEvent,

  createGame,

  updateGame,

  deleteGame

} from '../services/gameService'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import { runAsync } from '@/utils/request'
import { isScheduledGame } from '@/utils/gameLifecycle'


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

          let response

          try {
            response = await getScheduledGamesByEvent(
              eventContextStore.currentEventId
            )
          } catch (scheduledErr) {
            console.warn(
              'Scheduled games filter unavailable, falling back to full list.',
              scheduledErr
            )
            response = await getGamesByEvent(
              eventContextStore.currentEventId
            )
          }

          games.value = (response?.data || []).filter(
            isScheduledGame
          )
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
