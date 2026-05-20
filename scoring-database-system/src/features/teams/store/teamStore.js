import { computed, ref } from 'vue'

import {

  fetchTeams,

  createTeam,

  updateTeam,

  deleteTeam

} from '../services/teamService'


const teams = ref([])

const loading = ref(false)

const error = ref(null)


const totalTeams = computed(() => {
  return teams.value.length
})


const loadTeams = async () => {

  loading.value = true

  error.value = null

  try {

    teams.value =
      await fetchTeams()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to load teams.'

  } finally {

    loading.value = false
  }
}


const addTeam = async (
  payload
) => {

  try {

    await createTeam(payload)

    await loadTeams()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to create team.'
  }
}


const editTeam = async (
  teamId,
  payload
) => {

  try {

    await updateTeam(
      teamId,
      payload
    )

    await loadTeams()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to update team.'
  }
}


const removeTeam = async (
  teamId
) => {

  try {

    await deleteTeam(teamId)

    await loadTeams()

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Failed to delete team.'
  }
}


export function useTeamStore() {

  return {

    teams,

    loading,

    error,

    totalTeams,

    loadTeams,

    addTeam,

    editTeam,

    removeTeam
  }
}
