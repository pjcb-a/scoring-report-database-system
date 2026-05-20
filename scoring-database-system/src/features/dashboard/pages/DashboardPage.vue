<script setup>

import { onMounted } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {
  useEventContextStore
} from '@/features/events/store/eventContextStore'

import {
  useDashboardStore
} from '../store/dashboardStore'


/*
|--------------------------------------------------------------------------
| ROUTER
|--------------------------------------------------------------------------
*/

const router = useRouter()

/*
|--------------------------------------------------------------------------
| EVENT CONTEXT
|--------------------------------------------------------------------------
*/

const eventContextStore =
  useEventContextStore()

const {

  currentEvent

} = storeToRefs(
  eventContextStore
)

/*
|--------------------------------------------------------------------------
| DASHBOARD STORE
|--------------------------------------------------------------------------
*/

const dashboardStore =
  useDashboardStore()

const {

  totalSports,

  totalGames,

  totalScores,

  recentGames,

  recentWinners,

  loading

} = dashboardStore


/*
|--------------------------------------------------------------------------
| INITIALIZE
|--------------------------------------------------------------------------
*/

onMounted(async () => {

  if (!currentEvent.value) {

    router.push('/events')

    return
  }

  await dashboardStore.loadDashboard()
})

</script>

<template>

  <section class="dashboard-page">

    <div class="dashboard-header">

      <h1 class="dashboard-title">

        {{ currentEvent?.event_name }}

      </h1>

      <p class="dashboard-subtitle">

        Event Dashboard Overview

      </p>

    </div>

    <div
      v-if="loading"
      class="dashboard-loading"
    >
      Loading Dashboard...
    </div>

    <div
      v-else
      class="dashboard-grid"
    >

      <div class="dashboard-card">

        <h3>Total Sports</h3>

        <p>{{ totalSports }}</p>

      </div>

      <div class="dashboard-card">

        <h3>Total Games</h3>

        <p>{{ totalGames }}</p>

      </div>

      <div class="dashboard-card">

        <h3>Total Scores</h3>

        <p>{{ totalScores }}</p>

      </div>

    </div>

  </section>

</template>

<style scoped>

.dashboard-page {

  padding: 30px;
}

.dashboard-header {

  margin-bottom: 30px;
}

.dashboard-title {

  font-size: 32px;

  font-weight: 800;
}

.dashboard-subtitle {

  margin-top: 6px;

  color: var(--text-muted);
}

.dashboard-loading {

  padding: 30px;

  text-align: center;
}

.dashboard-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;
}

.dashboard-card {

  background-color: var(--white);

  padding: 24px;

  border-radius: var(--radius-lg);

  border:
    1px solid var(--border-color);
}

.dashboard-card h3 {

  font-size: 16px;

  margin-bottom: 12px;
}

.dashboard-card p {

  font-size: 30px;

  font-weight: 700;
}

</style>