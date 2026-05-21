import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getJudgeScoresByEvent,
  createJudgeScoreService,
  finalizeJudgeGameService
} from '../services/judgingService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'

export const useJudgingStore = defineStore(
  'judgingStore',
  () => {

    /*
    |--------------------------------------------------------------------------
    | STATE
    |--------------------------------------------------------------------------
    */
    const judgeScores = ref([])
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
    | LOAD JUDGE SCORES
    |--------------------------------------------------------------------------
    */
    const loadJudgeScores = async () => {
        if (!currentEventId.value) {
          judgeScores.value = []
          return
        }

        loading.value = true
        error.value = null

        try {
          const response = await getJudgeScoresByEvent(currentEventId.value)
          
          // FIX: Prevent HTML strings from crashing the router
          judgeScores.value = Array.isArray(response) ? response : []

        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to load judge scores.'
          judgeScores.value = []
        } finally {
          loading.value = false
        }
      }

    /*
    |--------------------------------------------------------------------------
    | CREATE JUDGE SCORE
    |--------------------------------------------------------------------------
    */
    const createJudgeScore = async (payload) => {
        loading.value = true
        error.value = null

        try {
          await createJudgeScoreService(payload)
          await loadJudgeScores()
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to create judge score.'
          throw err
        } finally {
          loading.value = false
        }
      }

    /*
    |--------------------------------------------------------------------------
    | FINALIZE JUDGE GAME
    |--------------------------------------------------------------------------
    */
    const finalizeJudgeGame = async (gameId, payload) => {
        loading.value = true
        error.value = null

        try {
          await finalizeJudgeGameService(gameId, payload)
          await loadJudgeScores()
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to finalize judge game.'
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
      judgeScores,
      loading,
      error,

      /*
      |--------------------------------------------------------------------------
      | METHODS
      |--------------------------------------------------------------------------
      */
      loadJudgeScores,
      createJudgeScore,
      finalizeJudgeGame
    }
  }
)