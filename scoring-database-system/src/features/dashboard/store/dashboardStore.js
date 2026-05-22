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
      computed(() => {

        return eventContextStore
          .currentEvent
      })

    const currentEventId =
      computed(() => {

        return eventContextStore
          .currentEventId
      })

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

    const totalTeams =
      computed(() => {

        return statistics.value
          .total_teams || 0
      })

    const recentGames =
      computed(() => {

        return Array.isArray(games.value)

          ? games.value.slice(-5)

          : []
      })

    /*
    --------------------------------------------------------------------------
    RESET DASHBOARD
    --------------------------------------------------------------------------
    */

    const resetDashboard =
      () => {

        sports.value = []

        games.value = []

        scores.value = []

        statistics.value = {}

        error.value = null
      }

    /*
    --------------------------------------------------------------------------
    LOAD DASHBOARD
    --------------------------------------------------------------------------
    */

    const loadDashboard =
      async () => {

        /*
        ----------------------------------------------------------------------
        VALIDATE EVENT
        ----------------------------------------------------------------------
        */

        if (!currentEventId.value) {

          resetDashboard()

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
            response?.data?.data || {}

          /*
          --------------------------------------------------------------------
          NORMALIZED STATE
          --------------------------------------------------------------------
          */

          sports.value =

            Array.isArray(
              dashboard.sports
            )

              ? dashboard.sports

              : []

          games.value =

            Array.isArray(
              dashboard.games
            )

              ? dashboard.games

              : []

          scores.value =

            Array.isArray(
              dashboard.scores
            )

              ? dashboard.scores

              : []

          statistics.value =

            dashboard.statistics || {}

        } catch (err) {

          console.error(err)

          resetDashboard()

          error.value =

            err.response?.data?.message

            ||

            'Failed to load dashboard.'

        } finally {

          loading.value = false
        }
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

      totalTeams,

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