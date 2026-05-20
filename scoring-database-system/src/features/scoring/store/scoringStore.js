import { computed, ref } from 'vue'

import {

  fetchScores,

  createScore,

  updateScore,

  deleteScore,

  fetchGames,

  fetchTeams

} from '../services/scoringService'


const scores = ref([])

const games = ref([])

const teams = ref([])

const loading = ref(false)

const error = ref(null)


const totalScores = computed(() => {
  return scores.value.length
})

const winnerScores = computed(() => {

  return scores.value.filter(
    score => score.isWinner
  ).length
})


const loadScores = async () => {

  loading.value = true

  error.value = null

  try {

    scores.value =
      await fetchScores()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to load scores.'

  } finally {

    loading.value = false
  }
}


const loadGames = async () => {

  try {

    games.value =
      await fetchGames()

  } catch (err) {

    console.error(err)
  }
}


const loadTeams = async () => {

  try {

    teams.value =
      await fetchTeams()

  } catch (err) {

    console.error(err)
  }
}


const addScore = async (
  payload
) => {

  try {

    await createScore(payload)

    await loadScores()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to create score.'
  }
}


const editScore = async (
  scoreId,
  payload
) => {

  try {

    await updateScore(
      scoreId,
      payload
    )

    await loadScores()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to update score.'
  }
}


const removeScore = async (
  scoreId
) => {

  try {

    await deleteScore(scoreId)

    await loadScores()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to delete score.'
  }
}


export function useScoringStore() {

  return {

    scores,

    games,

    teams,

    loading,

    error,

    totalScores,

    winnerScores,

    loadScores,

    loadGames,

    loadTeams,

    addScore,

    editScore,

    removeScore
  }
}
