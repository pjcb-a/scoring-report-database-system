<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import EventCard from '../components/EventCard.vue'

import EventForm from '../components/EventForm.vue'

import { useEventStore } from '../store/eventStore'

import {

  useEventContextStore

} from '../store/eventContextStore'

const router = useRouter()
/*
------------------------------------------------------------------------------
STORES
------------------------------------------------------------------------------
*/

const eventStore =
  useEventStore()

const eventContextStore =
  useEventContextStore()

/*
------------------------------------------------------------------------------
STATE
------------------------------------------------------------------------------
*/

const showEventForm = ref(false)

/*
------------------------------------------------------------------------------
COMPUTED
------------------------------------------------------------------------------
*/

const events =
  computed(() => {

    return eventStore.events
  })

const loading =
  computed(() => {

    return eventStore.loading
  })

const selectedEventId =
  computed(() => {

    return eventContextStore
      .currentEventId
  })

/*
------------------------------------------------------------------------------
LOAD EVENTS
------------------------------------------------------------------------------
*/

const loadEvents =
  async () => {

    await eventStore.loadEvents()
  }

/*
------------------------------------------------------------------------------
SELECT EVENT
------------------------------------------------------------------------------
*/

const selectEvent =
  async (event) => {

    /*
    --------------------------------------------------------------------------
    SET ACTIVE EVENT
    --------------------------------------------------------------------------
    */

    eventContextStore
      .setCurrentEvent(event)

    /*
    --------------------------------------------------------------------------
    OPEN EVENT DASHBOARD
    --------------------------------------------------------------------------
    */

    await router.push(

      `/events/${event.event_id}/dashboard`
    )
  }
/*
------------------------------------------------------------------------------
CREATE EVENT
------------------------------------------------------------------------------
*/

const handleCreateEvent =
  async (payload) => {

    try {

      /*
      ------------------------------------------------------------------------
      CREATE EVENT
      ------------------------------------------------------------------------
      */

      const createdEvent =

        await eventStore.createEvent(
          payload
        )

      /*
      ------------------------------------------------------------------------
      REFRESH EVENTS
      ------------------------------------------------------------------------
      */

      await eventStore.loadEvents()

      /*
      ------------------------------------------------------------------------
      CLOSE MODAL
      ------------------------------------------------------------------------
      */

      showEventForm.value = false

      /*
      ------------------------------------------------------------------------
      AUTO SELECT EVENT
      ------------------------------------------------------------------------
      */

      if (createdEvent) {

        eventContextStore
          .setCurrentEvent(
            createdEvent
          )
      }

      /*
      ------------------------------------------------------------------------
      REDIRECT TO EVENTS PAGE
      ------------------------------------------------------------------------
      */

      await router.push('/events')

    } catch (error) {

      console.error(error)
    }
  }

  /*
------------------------------------------------------------------------------
DELETE EVENT
------------------------------------------------------------------------------
*/

const handleDeleteEvent =
  async (eventId) => {

    try {

      await eventStore.removeEvent(
        eventId
      )

      if (

        selectedEventId.value === eventId
      ) {

        eventContextStore
          .clearCurrentEvent()
      }

      await router.push('/events')

    } catch (error) {

      console.error(error)
    }
  }

/*
------------------------------------------------------------------------------
MOUNTED
------------------------------------------------------------------------------
*/

onMounted(async () => {

  await loadEvents()
})
</script>

<template>
  <section class="event-page">

    <!-- ACTIVE EVENT -->

    <div

      v-if="eventContextStore.currentEvent"

      class="active-event-banner"
    >
      <div class="active-event-content">

        <i class="fa-solid fa-calendar-days"></i>

        <span>

          Current Event:

          {{ eventContextStore.currentEventName }}

        </span>
      </div>
    </div>

    <!-- HEADER -->

    <div class="event-page-header">

      <div>
        <h1>
          Events
        </h1>

        <p>
          Manage all sports events.
        </p>
      </div>

      <button

        class="add-event-btn"

        @click="showEventForm = true"
      >
        <i class="fa-solid fa-plus"></i>

        Add Event
      </button>
    </div>

    <!-- EVENT FORM -->

    <EventForm

      v-if="showEventForm"

      @close="showEventForm = false"

      @save="handleCreateEvent"
    />

    <!-- LOADING -->

    <div

      v-if="loading"

      class="loading-state"
    >
      Loading events...
    </div>

    <!-- EMPTY -->

    <div

      v-else-if="!events.length"

      class="empty-state"
    >
      No events available.
    </div>

    <!-- EVENTS -->

    <div

      v-else

      class="event-grid"
    >
      <EventCard

        v-for="event in events"

        :key="event.event_id"

        :event="event"

        :is-active="
          selectedEventId === event.event_id
        "

        @select="selectEvent"
        @delete="handleDeleteEvent"
      />
    </div>
  </section>
</template>

<style scoped>
.event-page {

  display: flex;

  flex-direction: column;

  gap: 1.5rem;
}

.event-page-header {

  display: flex;

  align-items: center;

  justify-content: space-between;
}

.event-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(320px, 1fr));

  gap: 1.25rem;
}

.active-event-banner {

  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 1rem 1.25rem;

  border-radius: 14px;

  background: linear-gradient(
    135deg,
    #2563eb,
    #1d4ed8
  );

  color: white;
}

.active-event-content {

  display: flex;

  align-items: center;

  gap: 0.75rem;

  font-weight: 600;
}

.add-event-btn {

  display: flex;

  align-items: center;

  gap: 0.6rem;

  padding: 0.8rem 1rem;

  border: none;

  border-radius: 10px;

  background: #2563eb;

  color: white;

  cursor: pointer;
}

.loading-state,
.empty-state {

  padding: 2rem;

  border-radius: 12px;

  background: white;

  text-align: center;
}
</style>