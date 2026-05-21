import { defineStore } from 'pinia'

import { computed, ref } from 'vue'

import {

  fetchDashboardSummaryByEvent

} from '../services/dashboardService'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'


export const useDashboardStore = defineStore(

  'dashboardStore',

  () => {

    /*
    --------------------------------------------------------------------------
    EVENT CONTEXT
    --------------------------------------------------------------------------
    */

    const eventContextStore =
      useEventContextStore()

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const sports = ref([])

    const games = ref([])

    const scores = ref([])

    const statistics = ref({})

    const loading = ref(false)

    const error = ref(null)

    /*
    --------------------------------------------------------------------------
    COMPUTED
    --------------------------------------------------------------------------
    */

    const currentEvent =
      computed(() =>
        eventContextStore.currentEvent
      )

    const currentEventId =
      computed(() =>
        eventContextStore.currentEventId
      )

    const totalSports =
      computed(() => {

        return statistics.value
          .total_sports || 0
      })

    const totalGames =
      computed(() => {

        return statistics.value
          .total_games || 0
      })

    const totalScores =
      computed(() => {

        return statistics.value
          .total_scores || 0
      })

    const recentGames =
      computed(() => {

        return games.value.slice(-5)
      })

    /*
    --------------------------------------------------------------------------
    LOAD DASHBOARD
    --------------------------------------------------------------------------
    */

    const loadDashboard =
      async () => {

        if (!currentEventId.value) {
          return
        }

        loading.value = true

        error.value = null

        try {

          const response =

            await fetchDashboardSummaryByEvent(

              currentEventId.value
            )

          /*
          --------------------------------------------------------------------
          NORMALIZED RESPONSE
          --------------------------------------------------------------------
          */

          const dashboard =
            response.data || {}

          sports.value =
            dashboard.sports || []

          games.value =
            dashboard.games || []

          scores.value =
            dashboard.scores || []

          statistics.value =
            dashboard.statistics || {}

        } catch (err) {

          console.error(err)

          error.value =

            err.response?.data?.message

            ||

            'Failed to load dashboard.'

        } finally {

          loading.value = false
        }
      }

    /*
    --------------------------------------------------------------------------
    RESET DASHBOARD
    --------------------------------------------------------------------------
    */

    const resetDashboard = () => {

      sports.value = []

      games.value = []

      scores.value = []

      statistics.value = {}

      loading.value = false

      error.value = null
    }

    return {

      /*
      ------------------------------------------------------------------------
      EVENT
      ------------------------------------------------------------------------
      */

      currentEvent,

      currentEventId,

      /*
      ------------------------------------------------------------------------
      STATE
      ------------------------------------------------------------------------
      */

      sports,

      games,

      scores,

      statistics,

      loading,

      error,

      /*
      ------------------------------------------------------------------------
      COMPUTED
      ------------------------------------------------------------------------
      */

      totalSports,

      totalGames,

      totalScores,

      recentGames,

      /*
      ------------------------------------------------------------------------
      METHODS
      ------------------------------------------------------------------------
      */

      loadDashboard,

      resetDashboard
    }
  }
)