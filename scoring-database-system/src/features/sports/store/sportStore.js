import { computed, ref } from 'vue'

import {

  fetchSports,

  createSport,

  updateSport,

  deleteSport,

  fetchScoringTypes

} from '../services/sportService'


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const sports = ref([])

const scoringTypes = ref([])

const loading = ref(false)

const error = ref(null)


/*
|--------------------------------------------------------------------------
| GETTERS
|--------------------------------------------------------------------------
*/

const totalSports = computed(() => {
  return sports.value.length
})

const componentSports = computed(() => {

  return sports.value.filter(
    sport =>
      sport.scoring_type ===
      'Component Score'
  ).length
})


/*
|--------------------------------------------------------------------------
| ACTIONS
|--------------------------------------------------------------------------
*/

const loadSports = async () => {

  loading.value = true

  error.value = null

  try {

    sports.value =
      await fetchSports()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to load sports.'

  } finally {

    loading.value = false
  }
}


const loadScoringTypes = async () => {

  try {

    scoringTypes.value =
      await fetchScoringTypes()

  } catch (err) {

    console.error(err)
  }
}


const addSport = async (
  payload
) => {

  try {

    await createSport(payload)

    await loadSports()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to create sport.'
  }
}


const editSport = async (
  sportId,
  payload
) => {

  try {

    await updateSport(
      sportId,
      payload
    )

    await loadSports()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to update sport.'
  }
}


const removeSport = async (
  sportId
) => {

  try {

    await deleteSport(sportId)

    await loadSports()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to delete sport.'
  }
}


/*
|--------------------------------------------------------------------------
| STORE EXPORT
|--------------------------------------------------------------------------
*/

export function useSportStore() {

  return {

    sports,

    scoringTypes,

    loading,

    error,

    totalSports,

    componentSports,

    loadSports,

    loadScoringTypes,

    addSport,

    editSport,

    removeSport
  }
}
