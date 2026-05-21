import { defineStore } from 'pinia'

import { ref, computed } from 'vue'

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

    const loading = ref(false)

    const error = ref(null)

    /*
    --------------------------------------------------------------------------
    EVENT CONTEXT
    --------------------------------------------------------------------------
    */

    const eventContextStore =
      useEventContextStore()

    const currentEventId =
  computed(() => {

    return eventContextStore
      .currentEventId
  })

    /*
------------------------------------------------------------------------------
LOAD EVENT SPORTS
------------------------------------------------------------------------------
*/

const loadSports =
  async () => {

    /*
    --------------------------------------------------------------------------
    VALIDATE EVENT
    --------------------------------------------------------------------------
    */

    if (!currentEventId.value) {

      sports.value = []

      return
    }

    loading.value = true

    error.value = null

    try {

      const response =

        await getSportsByEvent(

          currentEventId.value
        )

      sports.value =

        Array.isArray(response.data)

          ? response.data

          : []

    } catch (err) {

      console.error(err)

      sports.value = []

      error.value =

        err.message ||

        'Failed to load sports.'

    } finally {

      loading.value = false
    }
  }

    /*
------------------------------------------------------------------------------
ADD SPORT TO EVENT
------------------------------------------------------------------------------
*/

const addSport =
  async (payload) => {

    if (!currentEventId.value) {
      return
    }

    try {

      await addSportToEvent(

        currentEventId.value,

        payload
      )

      /*
      ------------------------------------------------------------------------
      REFRESH SPORTS
      ------------------------------------------------------------------------
      */

      await loadSports()

    } catch (err) {

      console.error(err)

      throw err
    }
  }

    /*
------------------------------------------------------------------------------
REMOVE EVENT SPORT
------------------------------------------------------------------------------
*/

const deleteSport =
  async (eventSportId) => {

    try {

      await removeEventSport(
        eventSportId
      )

      /*
      ------------------------------------------------------------------------
      OPTIMISTIC UI UPDATE
      ------------------------------------------------------------------------
      */

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

      loading,

      error,

      /*
      ------------------------------------------------------------------------
      METHODS
      ------------------------------------------------------------------------
      */

      loadSports,

      addSport,

      deleteSport
    }
  }
)