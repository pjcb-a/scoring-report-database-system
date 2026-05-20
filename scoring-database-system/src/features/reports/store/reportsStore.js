import { defineStore } from 'pinia'

import { ref } from 'vue'

import {

  getEventRankings

} from '../services/reportService'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'


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

    const eventContextStore =
      useEventContextStore()

    /*
    --------------------------------------------------------------------------
    LOAD REPORTS
    --------------------------------------------------------------------------
    */

    const loadRankings =
      async () => {

        if (
          !eventContextStore.currentEventId
        ) {
          return
        }

        loading.value = true

        error.value = null

        try {

          const response =
            await getEventRankings(

              eventContextStore.currentEventId
            )

          rankings.value =
            response.data || []

        } catch (err) {

          console.error(err)

          error.value =
            err.message ||
            'Failed to load rankings.'

        } finally {

          loading.value = false
        }
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