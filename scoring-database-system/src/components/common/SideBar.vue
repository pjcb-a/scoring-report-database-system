<script setup>

import { storeToRefs } from 'pinia'

import {
  useEventContextStore
}
from '@/features/events/store/eventContextStore'


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

</script>

<template>

  <aside class="sidebar">

    <!--
    ------------------------------------------------------------------------
    SIDEBAR HEADER
    ------------------------------------------------------------------------
    -->

    <div class="sidebar-header">

      <h1 class="sidebar-logo">
        SRDS
      </h1>

      <p class="sidebar-subtitle">
        Sports Reporting
      </p>

    </div>

    <!--
    ------------------------------------------------------------------------
    NAVIGATION
    ------------------------------------------------------------------------
    -->

    <nav class="sidebar-nav">

      <!-- EVENTS -->

      <router-link
        to="/events"
        class="sidebar-link"
      >
        Events
      </router-link>

      <!-- DASHBOARD -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/dashboard`"
        class="sidebar-link"
      >
        Dashboard
      </router-link>

      <!-- SPORTS -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/sports`"
        class="sidebar-link"
      >
        Sports
      </router-link>

      <!-- TEAMS -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/teams`"
        class="sidebar-link"
      >
        Teams
      </router-link>

      <!-- GAMES -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/games`"
        class="sidebar-link"
      >
        Games
      </router-link>

      <!-- SCORING -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/scoring`"
        class="sidebar-link"
      >
        Scoring
      </router-link>

      <!-- JUDGING -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/judging`"
        class="sidebar-link"
      >
        Judging
      </router-link>

      <!-- REPORTS -->

      <router-link
        v-if="currentEventId"
        :to="`/events/${currentEventId}/reports`"
        class="sidebar-link"
      >
        Reports
      </router-link>

    </nav>

  </aside>

</template>

<style scoped>

.sidebar {

  width: 260px;

  min-height: 100vh;

  background-color: var(--adnu-blue-dark);

  border-right: 1px solid var(--border-color);

  padding: 20px;

  border-radius: 0 15px 15px 0;
}

.sidebar-header {

  margin-bottom: 30px;
}

.sidebar-logo {

  font-size: 28px;

  font-weight: 800;

  color: var(--adnu-danger-light);
}

.sidebar-subtitle {

  color: var(--text-muted);

  font-size: 13px;
}

.sidebar-nav {

  display: flex;

  flex-direction: column;

  gap: 10px;
}

.sidebar-link {

  padding: 12px 16px;

  border-radius: var(--radius-md);

  transition: var(--transition-fast);

  color: var(--white);
}

.sidebar-link:hover {

  background-color: var(--adnu-blue-light);

  color: var(--text-main);
}

.sidebar-link.router-link-active {

  background-color: var(--adnu-blue-light);

  color: var(--text-main);
}

</style>