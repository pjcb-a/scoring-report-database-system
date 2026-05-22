import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getScoresByEvent,
  createScoreService,
  finalizeGameService
} from '../services/scoringService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { useGameStore } from '@/features/games/store/gameStore'

export const useScoringStore = defineStore(
  'scoringStore',
  () => {

    /*
    |--------------------------------------------------------------------------
    | STATE
    |--------------------------------------------------------------------------
    */
    const scores = ref([])
    const loading = ref(false)
    const error = ref(null)

    /*
    |--------------------------------------------------------------------------
    | EVENT CONTEXT
    |--------------------------------------------------------------------------
    */
    const eventContextStore = useEventContextStore()

    const currentEventId = computed(() => {
        return eventContextStore.currentEventId
    })

    /*
    |--------------------------------------------------------------------------
    | LOAD SCORES
    |--------------------------------------------------------------------------
    */
    const loadScores = async () => {
        if (!currentEventId.value) {
          scores.value = []
          return
        }

        loading.value = true
        error.value = null

        try {
          const response = await getScoresByEvent(currentEventId.value)
          
          // FIX: Prevent HTML strings from crashing the router
          scores.value = Array.isArray(response) ? response : []

        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to load scores.'
          scores.value = []
        } finally {
          loading.value = false
        }
      }

    /*
    |--------------------------------------------------------------------------
    | CREATE SCORE
    |--------------------------------------------------------------------------
    */
    const createScore = async (payload) => {
        loading.value = true
        error.value = null

        try {
          await createScoreService(payload)
          await loadScores()
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to create score.'
          throw err
        } finally {
          loading.value = false
        }
      }

    /*
    |--------------------------------------------------------------------------
    | FINALIZE GAME
    |--------------------------------------------------------------------------
    */
    const finalizeGame = async (gameId, payload) => {
        loading.value = true
        error.value = null

        try {
          await finalizeGameService(gameId, payload)
          const gameStore = useGameStore()
          await gameStore.loadGames()
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to finalize game.'
          throw err
        } finally {
          loading.value = false
        }
      }

    return {
      /*
      |--------------------------------------------------------------------------
      | STATE
      |--------------------------------------------------------------------------
      */
      scores,
      loading,
      error,

      /*
      |--------------------------------------------------------------------------
      | METHODS
      |--------------------------------------------------------------------------
      */
      loadScores,
      createScore,
      finalizeGame
    }
  }
)