import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  getJudgeScoresByEvent,
  createJudgeScoreService,
  finalizeJudgeGameService,
  getJudgesByEvent
} from '../services/judgingService'
import { getGamesByEvent } from '@/features/games/services/gameService'
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
    const games = ref([])
    const judges = ref([])
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
    | COMPUTED - PENDING & FINALIZED GAMES
    |--------------------------------------------------------------------------
    */
    const pendingGames = computed(() => {
      return games.value.filter(game => 
        game.sport?.scoring_type === 'component' && 
        game.status !== 'finalized'
      )
    })

    const finalizedGames = computed(() => {
      return games.value.filter(game => 
        game.sport?.scoring_type === 'component' && 
        game.status === 'finalized'
      )
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
    | LOAD GAMES
    |--------------------------------------------------------------------------
    */
    const loadGames = async () => {
        if (!currentEventId.value) {
          games.value = []
          return
        }

        loading.value = true
        error.value = null

        try {
          const response = await getGamesByEvent(currentEventId.value)
          games.value = response?.data || []
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to load games.'
          games.value = []
        } finally {
          loading.value = false
        }
      }

    /*
    |--------------------------------------------------------------------------
    | LOAD JUDGES
    |--------------------------------------------------------------------------
    */
    const loadJudges = async () => {
        if (!currentEventId.value) {
          judges.value = []
          return
        }

        try {
          const response = await getJudgesByEvent(currentEventId.value)
          judges.value = response?.data || []
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to load judges.'
          judges.value = []
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
          await finalizeJudgeGameService(gameId, payload)
          await loadGames()
        } catch (err) {
          console.error(err)
          error.value = err.message || 'Failed to finalize game.'
          throw err
        } finally {
          loading.value = false
        }
      }

    /*
    |--------------------------------------------------------------------------
    | FINALIZE JUDGE GAME (Legacy - keeping for compatibility)
    |--------------------------------------------------------------------------
    */
    const finalizeJudgeGame = async (gameId, payload) => {
        return finalizeGame(gameId, payload)
      }

    return {
      /*
      |--------------------------------------------------------------------------
      | STATE
      |--------------------------------------------------------------------------
      */
      judgeScores,
      games,
      judges,
      loading,
      error,

      /*
      |--------------------------------------------------------------------------
      | COMPUTED
      |--------------------------------------------------------------------------
      */
      pendingGames,
      finalizedGames,

      /*
      |--------------------------------------------------------------------------
      | METHODS
      |--------------------------------------------------------------------------
      */
      loadJudgeScores,
      loadGames,
      loadJudges,
      createJudgeScore,
      finalizeGame,
      finalizeJudgeGame
    }
  }
)