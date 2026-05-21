import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getEventRankings } from '../services/reportsService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { runAsync } from '@/utils/request'

export const useReportStore = defineStore(
  'reportStore',
  () => {
    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */
    const rankings = ref([])
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
    LOAD REPORTS
    --------------------------------------------------------------------------
    */
    const loadRankings = async () => {
      if (!eventContextStore.currentEventId) {
        return
      }

      await runAsync({ loading, error }, async () => {
        const response = await getEventRankings(eventContextStore.currentEventId)
        rankings.value = response.data || []
      })
    }

    return {
      /*
      ------------------------------------------------------------------------
      STATE
      ------------------------------------------------------------------------
      */
      rankings,
      loading,
      error,

      /*
      ------------------------------------------------------------------------
      METHODS
      ------------------------------------------------------------------------
      */
      loadRankings
    }
  }
)