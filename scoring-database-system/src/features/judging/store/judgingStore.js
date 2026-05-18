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

  try {

    judgeScores.value =
      await fetchJudgeScores()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to load judge scores.'

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
  }
}


const loadCriteria = async () => {

  try {

    criteria.value =
      await fetchCriteria()

  } catch (err) {

    console.error(err)
  }
}


const loadJudges = async () => {

  try {

    judges.value =
      await fetchJudges()

  } catch (err) {

    console.error(err)
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