import { computed, ref } from 'vue'

import {
  fetchDashboardSummary
} from '../services/dashboardService'


const events = ref([])

const sports = ref([])

const games = ref([])

const scores = ref([])

const loading = ref(false)

const error = ref(null)


const totalEvents = computed(() => {
  return events.value.length
})

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


const loadDashboard = async () => {

  loading.value = true

  error.value = null

  try {

    const data =
      await fetchDashboardSummary()

    events.value = data.events

    sports.value = data.sports

    games.value = data.games

    scores.value = data.scores

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to load dashboard.'

  } finally {

    loading.value = false
  }
}


export function useDashboardStore() {

  return {

    events,

    sports,

    games,

    scores,

    loading,

    error,

    totalEvents,

    totalSports,

    totalGames,

    totalScores,

    recentGames,

    recentWinners,

    loadDashboard
  }
}
