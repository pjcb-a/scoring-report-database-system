import { computed, ref } from 'vue'

import {

  fetchJudgeScores,

  createJudgeScore,

  updateJudgeScore,

  deleteJudgeScore,

  fetchGameScores,

  fetchCriteria,

  fetchJudges

} from '../services/judgingService'


const judgeScores = ref([])

const gameScores = ref([])

const criteria = ref([])

const judges = ref([])

const loading = ref(false)

const error = ref(null)


const totalJudgeScores = computed(() => {
  return judgeScores.value.length
})

const totalJudges = computed(() => {
  return judges.value.length
})


const loadJudgeScores = async () => {

  loading.value = true
  error.value = null

  try {

    judgeScores.value =
      await fetchJudgeScores()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to load judge scores.'

  } finally {

    loading.value = false
  }
}


const loadGameScores = async () => {

  try {

    gameScores.value =
      await fetchGameScores()

  } catch (err) {

    console.error(err)
    error.value =
      err.message || 'Failed to load game scores.'
  }
}


const loadCriteria = async () => {

  try {

    criteria.value =
      await fetchCriteria()

  } catch (err) {

    console.error(err)
    error.value =
      err.message || 'Failed to load criteria.'
  }
}


const loadJudges = async () => {

  try {

    judges.value =
      await fetchJudges()

  } catch (err) {

    console.error(err)
    error.value =
      err.message || 'Failed to load judges.'
  }
}


const addJudgeScore = async (
  payload
) => {

  try {

    await createJudgeScore(payload)

    await loadJudgeScores()

  } catch (err) {

    console.error(err)
    error.value =
      err.message || 'Failed to create judge score.'
  }
}


const editJudgeScore = async (
  scoreComponentId,
  payload
) => {

  try {

    await updateJudgeScore(
      scoreComponentId,
      payload
    )

    await loadJudgeScores()

  } catch (err) {

    console.error(err)
    error.value =
      err.message || 'Failed to update judge score.'
  }
}


const removeJudgeScore = async (
  scoreComponentId
) => {

  try {

    await deleteJudgeScore(
      scoreComponentId
    )

    await loadJudgeScores()

  } catch (err) {

    console.error(err)
    error.value =
      err.message || 'Failed to delete judge score.'
  }
}


export function useJudgingStore() {

  return {

    judgeScores,

    gameScores,

    criteria,

    judges,

    loading,

    error,

    totalJudgeScores,

    totalJudges,

    loadJudgeScores,

    loadGameScores,

    loadCriteria,

    loadJudges,

    addJudgeScore,

    editJudgeScore,

    removeJudgeScore
  }
}
