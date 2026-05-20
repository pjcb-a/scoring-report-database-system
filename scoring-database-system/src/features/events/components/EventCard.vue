<script setup>

import { computed } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import Badge from '@/components/ui/Badge.vue'

import {
  useEventContextStore
}
from '@/features/events/store/eventContextStore'


/*
|--------------------------------------------------------------------------
| PROPS
|--------------------------------------------------------------------------
*/

const props = defineProps({

  event: {
    type: Object,
    required: true
  }
})

/*
|--------------------------------------------------------------------------
| ROUTER
|--------------------------------------------------------------------------
*/

const router = useRouter()

/*
|--------------------------------------------------------------------------
| GLOBAL EVENT CONTEXT
|--------------------------------------------------------------------------
*/

const eventContextStore =
  useEventContextStore()

const {

  currentEventId

} = storeToRefs(
  eventContextStore
)

/*
|--------------------------------------------------------------------------
| COMPUTED
|--------------------------------------------------------------------------
*/

const badgeVariant = computed(() => {

  switch (props.event.status) {

    case 'Active':
      return 'success'

    case 'Completed':
      return 'primary'

    default:
      return 'warning'
  }
})

const isCurrentEvent = computed(() => {

  return (
    currentEventId.value ===
    props.event.event_id
  )
})

/*
|--------------------------------------------------------------------------
| METHODS
|--------------------------------------------------------------------------
*/

const formatDate = (date) => {

  if (!date) return 'N/A'

  return new Date(date)
    .toLocaleDateString()
}

const selectEvent = () => {

  /*
  --------------------------------------------------------------------------
  SET GLOBAL EVENT CONTEXT
  --------------------------------------------------------------------------
  */

  eventContextStore.setCurrentEvent(
    props.event
  )

  /*
  --------------------------------------------------------------------------
  REDIRECT TO EVENT DASHBOARD
  --------------------------------------------------------------------------
  */

  router.push(

    `/events/${props.event.event_id}/dashboard`
  )
}

</script>

<template>

  <div

    class="event-card card-base"

    :class="{
      'active-event-card':
      isCurrentEvent
    }"

    @click="selectEvent"
  >

    <!--
    ------------------------------------------------------------------------
    EVENT HEADER
    ------------------------------------------------------------------------
    -->

    <div class="event-card-top">

      <div>

        <div class="event-title-wrapper">

          <h2 class="event-title">

            {{ event.event_name }}

          </h2>

          <!-- ACTIVE EVENT INDICATOR -->

          <span
            v-if="isCurrentEvent"
            class="active-indicator"
          >
            Current Event
          </span>

        </div>

        <p class="event-date">

          {{ formatDate(event.start_day) }}

          -

          {{ formatDate(event.end_day) }}

        </p>

      </div>

      <!-- STATUS -->

      <Badge
        :variant="badgeVariant"
      >
        {{ event.status }}
      </Badge>

    </div>

    <!--
    ------------------------------------------------------------------------
    FOOTER
    ------------------------------------------------------------------------
    -->

    <div class="event-card-footer">

      <div class="event-meta">

        <span class="meta-label">
          Event ID
        </span>

        <span class="meta-value">
          #{{ event.event_id }}
        </span>

      </div>

      <!-- OPEN BUTTON -->

      <button
        class="open-event-button"
      >
        Open Event
      </button>

    </div>

  </div>

</template>

<style scoped>

.event-card {

  display: flex;

  flex-direction: column;

  gap: 20px;

  cursor: pointer;

  transition: var(--transition-fast);

  border: 2px solid transparent;
}

.event-card:hover {

  transform: translateY(-3px);

  border-color:
    var(--adnu-blue-light);
}

/*
|--------------------------------------------------------------------------
| ACTIVE EVENT CARD
|--------------------------------------------------------------------------
*/

.active-event-card {

  border-color:
    var(--adnu-danger-light);

  box-shadow:
    0 0 0 3px rgba(
      255,
      99,
      71,
      0.15
    );
}

/*
|--------------------------------------------------------------------------
| HEADER
|--------------------------------------------------------------------------
*/

.event-card-top {

  display: flex;

  justify-content: space-between;

  align-items: flex-start;
}

.event-title-wrapper {

  display: flex;

  align-items: center;

  gap: 10px;

  flex-wrap: wrap;
}

.event-title {

  font-size: 20px;

  font-weight: 700;
}

.active-indicator {

  background-color:
    var(--adnu-danger-light);

  color: white;

  padding: 4px 10px;

  border-radius: 999px;

  font-size: 11px;

  font-weight: 600;
}

.event-date {

  margin-top: 6px;

  color: var(--text-muted);

  font-size: 14px;
}

/*
|--------------------------------------------------------------------------
| FOOTER
|--------------------------------------------------------------------------
*/

.event-card-footer {

  padding-top: 14px;

  border-top:
    1px solid var(--border-color);

  display: flex;

  justify-content: space-between;

  align-items: center;
}

.event-meta {

  display: flex;

  flex-direction: column;

  gap: 4px;
}

.meta-label {

  font-size: 12px;

  color: var(--text-muted);
}

.meta-value {

  font-weight: 600;
}

/*
|--------------------------------------------------------------------------
| OPEN BUTTON
|--------------------------------------------------------------------------
*/

.open-event-button {

  border: none;

  background-color:
    var(--adnu-blue-light);

  color: var(--text-main);

  padding: 10px 14px;

  border-radius: var(--radius-md);

  cursor: pointer;

  font-weight: 600;

  transition: var(--transition-fast);
}

.open-event-button:hover {

  opacity: 0.9;
}

</style>