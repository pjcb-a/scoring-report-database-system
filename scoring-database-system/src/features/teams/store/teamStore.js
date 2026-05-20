import { defineStore } from 'pinia'

import { ref } from 'vue'

import {

  getTeamsByEvent,

  createTeam,

  updateTeam,

  deleteTeam

} from '../services/teamService'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'


export const useTeamStore = defineStore(

  'teamStore',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const teams = ref([])

    const loading = ref(false)

    const error = ref(null)

    /*
    --------------------------------------------------------------------------
    EVENT CONTEXT
    --------------------------------------------------------------------------
    */

    const eventContextStore =
      useEventContextStore()

    /*
    --------------------------------------------------------------------------
    LOAD TEAMS
    --------------------------------------------------------------------------
    */

    const loadTeams = async () => {

      if (
        !eventContextStore.currentEventId
      ) {
        return
      }

      loading.value = true

      error.value = null

      try {

        const response =
          await getTeamsByEvent(

            eventContextStore.currentEventId
          )

        teams.value =
          response.data || []

      } catch (err) {

        console.error(err)

        error.value =
          err.message ||
          'Failed to load teams.'

      } finally {

        loading.value = false
      }
    }

    /*
    --------------------------------------------------------------------------
    CREATE TEAM
    --------------------------------------------------------------------------
    */

    const addTeam = async (payload) => {

      try {

        await createTeam(

          eventContextStore.currentEventId,

          payload
        )

        await loadTeams()

      } catch (err) {

        console.error(err)

        throw err
      }
    }

    /*
    --------------------------------------------------------------------------
    UPDATE TEAM
    --------------------------------------------------------------------------
    */

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

        throw err
      }
    }

    /*
    --------------------------------------------------------------------------
    DELETE TEAM
    --------------------------------------------------------------------------
    */

    const removeTeam = async (
      teamId
    ) => {

      try {

        await deleteTeam(teamId)

        teams.value =
          teams.value.filter(

            team =>
              team.team_id !== teamId
          )

      } catch (err) {

        console.error(err)

        throw err
      }
    }

    return {

      /*
      ------------------------------------------------------------------------
      STATE
      ------------------------------------------------------------------------
      */

      teams,

      loading,

      error,

      /*
      ------------------------------------------------------------------------
      METHODS
      ------------------------------------------------------------------------
      */

      loadTeams,

      addTeam,

      editTeam,

      removeTeam
    }
  }
)