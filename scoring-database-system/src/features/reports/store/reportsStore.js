import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMatchReports } from '../services/reportsService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { runAsync } from '@/utils/request'

export const useReportStore = defineStore(
  'reportStore',
  () => {
    const matches = ref([])
    const loading = ref(false)
    const error = ref(null)

    const eventContextStore = useEventContextStore()

    const loadMatchReports = async () => {
      if (!eventContextStore.currentEventId) {
        return
      }

      await runAsync({ loading, error }, async () => {
        const response = await getMatchReports(
          eventContextStore.currentEventId
        )
        matches.value = response.data || []
      })
    }

    return {
      matches,
      loading,
      error,
      loadMatchReports
    }
  }
)
