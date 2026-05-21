import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getTeamsByEvent,
  createTeam,
  updateTeam,
  deleteTeam
} from '../services/teamService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { runAsync } from '@/utils/request'

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
    const eventContextStore = useEventContextStore()

    /*
    --------------------------------------------------------------------------
    LOAD TEAMS
    --------------------------------------------------------------------------
    */
    const loadTeams = async () => {
      if (!eventContextStore.currentEventId) {
        return
      }

      await runAsync({ loading, error }, async () => {
        const response = await getTeamsByEvent(eventContextStore.currentEventId)
        teams.value = response.data || []
      })
    }

    /*
    --------------------------------------------------------------------------
    CREATE TEAM
    --------------------------------------------------------------------------
    */
    const addTeam = async (payload) => {
      await runAsync(
        { loading, error },
        async () => {
          await createTeam(eventContextStore.currentEventId, payload)
          await loadTeams()
        },
        {
          showSuccessToast: true,
          successMessage: 'Team created successfully.'
        }
      )
    }

    /*
    --------------------------------------------------------------------------
    UPDATE TEAM
    --------------------------------------------------------------------------
    */
    const editTeam = async (teamId, payload) => {
      await runAsync(
        { loading, error },
        async () => {
          await updateTeam(teamId, payload)
          await loadTeams()
        },
        {
          showSuccessToast: true,
          successMessage: 'Team updated successfully.'
        }
      )
    }

    /*
    --------------------------------------------------------------------------
    DELETE TEAM
    --------------------------------------------------------------------------
    */
    const removeTeam = async (teamId) => {
      await runAsync(
        { loading, error },
        async () => {
          await deleteTeam(teamId)
          teams.value = teams.value.filter(
            team => team.team_id !== teamId
          )
        },
        {
          showSuccessToast: true,
          successMessage: 'Team deleted successfully.'
        }
      )
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