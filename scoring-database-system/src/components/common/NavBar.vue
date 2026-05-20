<script setup>

import { storeToRefs } from 'pinia'

import {
  useEventContextStore
} from '@/features/events/store/eventContextStore'


/*
|--------------------------------------------------------------------------
| EVENT CONTEXT
|--------------------------------------------------------------------------
*/

const eventContextStore =
  useEventContextStore()

const {

  currentEvent,

  currentEventName

} = storeToRefs(
  eventContextStore
)

</script>

<template>

  <header class="navbar">

    <div>

      <h1 class="navbar-title">

        {{ currentEventName }}

      </h1>

      <p
        v-if="currentEvent"
        class="event-indicator"
      >
        Current Event Active
      </p>

      <p
        v-else
        class="event-indicator"
      >
        No Event Selected
      </p>

    </div>

  </header>

</template>

<style scoped>

.navbar {

  width: 100%;

  padding: 20px 30px;

  background-color: var(--white);

  border-bottom:
    1px solid var(--border-color);

  display: flex;

  justify-content: space-between;

  align-items: center;
}

.navbar-title {

  font-size: 24px;

  font-weight: 700;

  color: var(--text-main);
}

.event-indicator {

  margin-top: 4px;

  font-size: 13px;

  color: var(--text-muted);
}

</style>