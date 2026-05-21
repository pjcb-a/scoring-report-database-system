import { computed, ref } from 'vue'

import {
  fetchDashboardSummaryByEvent
} from '../services/dashboardService'

import {
  useEventContextStore
} from '@/features/events/store/eventContextStore'


const sports = ref([])

const games = ref([])

const scores = ref([])

const loading = ref(false)

const error = ref(null)


/*
|--------------------------------------------------------------------------
| EVENT CONTEXT
|--------------------------------------------------------------------------
*/

let eventContextStore = null

function getEventContextStore() {
  if (!eventContextStore) {
    eventContextStore = useEventContextStore()
  }
  return eventContextStore
}


/*
|--------------------------------------------------------------------------
| COMPUTED
|--------------------------------------------------------------------------
*/

const currentEvent =
  computed(() =>
    getEventContextStore().currentEvent
  )

const currentEventId =
  computed(() =>
    getEventContextStore().currentEventId
  )

const totalSports = computed(() => {
  return sports.value.length
})

const totalGames = computed(() => {
  return games.value.length
})

const totalScores = computed(() => {
  return scores.value.length
})

const recentGames = computed(() => {

  return games.value.slice(-5)
})

const recentWinners = computed(() => {

  return scores.value.filter(
    score => score.isWinner
  ).slice(-5)
})


/*
|--------------------------------------------------------------------------
| LOAD DASHBOARD
|--------------------------------------------------------------------------
*/

const loadDashboard = async () => {

  if (!currentEventId.value) {
    return
  }

  loading.value = true

  error.value = null

  try {

    const data =
      await fetchDashboardSummaryByEvent(
        currentEventId.value
      )

    sports.value = data.sports || []

    games.value = data.games || []

    scores.value = data.scores || []

  } catch (err) {

    console.error(err)

    error.value =
      err.message ||
      'Failed to load dashboard.'

  } finally {

    loading.value = false
  }
}


export function useDashboardStore() {

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

    recentWinners,

    /*
    ------------------------------------------------------------------------
    METHODS
    ------------------------------------------------------------------------
    */

    loadDashboard
  }
}