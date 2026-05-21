import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { finalizeMatch } from '../services/scoringService'
import { getGamesByEvent } from '@/features/games/services/gameService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { runAsync } from '@/utils/request'

export const THRESHOLD_INCREMENTAL = 'Threshold Incremental'
export const COMPONENT_SCORE = 'Component Score'

const isNonComponentGame = (game) =>
  game.scoring_type !== COMPONENT_SCORE

export const useScoringStore = defineStore('scoringStore', () => {
  const games = ref([])
  const loading = ref(false)
  const error = ref(null)

  const eventContextStore = useEventContextStore()

  const pendingGames = computed(() =>
    games.value.filter(
      game => !game.is_finalized && isNonComponentGame(game)
    )
  )

  const finalizedGames = computed(() =>
    games.value.filter(
      game => game.is_finalized && isNonComponentGame(game)
    )
  )

  const loadGames = async () => {
    if (!eventContextStore.currentEventId) {
      return
    }

    await runAsync({ loading, error }, async () => {
      const response = await getGamesByEvent(
        eventContextStore.currentEventId
      )
      games.value = response.data || []
    })
  }

  const finalizeGame = async (gameId, payload) => {
    await runAsync(
      { loading, error },
      async () => {
        await finalizeMatch(gameId, payload)
        await loadGames()
      },
      {
        showSuccessToast: true,
        successMessage: 'Match finalized successfully.'
      }
    )
  }

  return {
    games,
    loading,
    error,
    pendingGames,
    finalizedGames,
    loadGames,
    finalizeGame
  }
})
