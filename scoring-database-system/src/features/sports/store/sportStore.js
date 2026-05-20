import { defineStore } from 'pinia'

import { ref } from 'vue'

import {

  getSports,

  getSportsByEvent,

  createSport,

  addSportToEvent,

  removeEventSport

} from '../services/sportService'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'


export const useSportStore = defineStore(

  'sportStore',

  () => {

    /*
    --------------------------------------------------------------------------
    STATE
    --------------------------------------------------------------------------
    */

    const sports = ref([])

    const masterSports = ref([])

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
    LOAD EVENT SPORTS
    --------------------------------------------------------------------------
    */

    const loadSports = async () => {

      if (
        !eventContextStore.currentEventId
      ) {
        return
      }

      loading.value = true

      error.value = null

      try {

        const response =
          await getSportsByEvent(

            eventContextStore.currentEventId
          )

        sports.value =
          response.data || []

      } catch (err) {

        console.error(err)

        error.value =
          err.message ||
          'Failed to load sports.'

      } finally {

        loading.value = false
      }
    }

    /*
    --------------------------------------------------------------------------
    LOAD MASTER SPORTS
    --------------------------------------------------------------------------
    */

    const loadMasterSports =
      async () => {

        try {

          const response =
            await getSports()

          masterSports.value =
            response.data || []

        } catch (err) {

          console.error(err)
        }
      }

    /*
    --------------------------------------------------------------------------
    CREATE MASTER SPORT
    --------------------------------------------------------------------------
    */

    const addMasterSport =
      async (payload) => {

        try {

          await createSport(payload)

          await loadMasterSports()

        } catch (err) {

          console.error(err)

          throw err
        }
      }

    /*
    --------------------------------------------------------------------------
    ADD SPORT TO EVENT
    --------------------------------------------------------------------------
    */

    const addSport =
      async (payload) => {

        try {

          await addSportToEvent(

            eventContextStore.currentEventId,

            payload
          )

          await loadSports()

        } catch (err) {

          console.error(err)

          throw err
        }
      }

    /*
    --------------------------------------------------------------------------
    REMOVE EVENT SPORT
    --------------------------------------------------------------------------
    */

    const deleteSport =
      async (eventSportId) => {

        try {

          await removeEventSport(
            eventSportId
          )

          sports.value =
            sports.value.filter(

              sport =>

                sport.event_sport_id
                !== eventSportId
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

      sports,

      masterSports,

      loading,

      error,

      /*
      ------------------------------------------------------------------------
      METHODS
      ------------------------------------------------------------------------
      */

      loadSports,

      loadMasterSports,

      addMasterSport,

      addSport,

      deleteSport
    }
  }
)