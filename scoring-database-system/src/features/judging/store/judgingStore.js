import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { finalizeMatch } from '@/features/scoring/services/scoringService'
import { getGamesByEvent } from '@/features/games/services/gameService'
import { getJudgesByEvent } from '../services/judgingService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { runAsync } from '@/utils/request'

export const COMPONENT_SCORE = 'Component Score'

const isComponentGame = (game) =>
  game.scoring_type === COMPONENT_SCORE

export const useJudgingStore = defineStore('judgingStore', () => {
  const games = ref([])
  const judges = ref([])
  const loading = ref(false)
  const error = ref(null)

  const eventContextStore = useEventContextStore()

  const pendingGames = computed(() =>
    games.value.filter(
      game => !game.is_finalized && isComponentGame(game)
    )
  )

  const finalizedGames = computed(() =>
    games.value.filter(
      game => game.is_finalized && isComponentGame(game)
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

  const loadJudges = async () => {
    if (!eventContextStore.currentEventId) {
      return
    }

    try {
      const response = await getJudgesByEvent(
        eventContextStore.currentEventId
      )
      judges.value = response.data || []
    } catch (err) {
      console.error(err)
    }
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
    judges,
    loading,
    error,
    pendingGames,
    finalizedGames,
    loadGames,
    loadJudges,
    finalizeGame
  }
})
