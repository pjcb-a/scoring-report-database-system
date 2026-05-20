<script setup>

import { onMounted } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useTeamStore

} from '../store/teamStore'


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
| TEAM STORE
|--------------------------------------------------------------------------
*/

const teamStore =
  useTeamStore()

const {

  teams,

  loading,

  error

} = storeToRefs(
  teamStore
)


/*
|--------------------------------------------------------------------------
| INITIALIZE
|--------------------------------------------------------------------------
*/

onMounted(async () => {

  /*
  --------------------------------------------------------------------------
  VALIDATE EVENT CONTEXT
  --------------------------------------------------------------------------
  */

  if (!currentEvent.value) {

    router.push('/events')

    return
  }

  /*
  --------------------------------------------------------------------------
  LOAD EVENT TEAMS
  --------------------------------------------------------------------------
  */

  await teamStore.loadTeams()
})

</script>

<template>

  <section class="team-page">

    <!--
    ------------------------------------------------------------------------
    HEADER
    ------------------------------------------------------------------------
    -->

    <div class="team-page-header">

      <h1 class="team-page-title">

        {{ currentEvent?.event_name }}

      </h1>

      <p class="team-page-subtitle">

        Event Teams

      </p>

    </div>

    <!--
    ------------------------------------------------------------------------
    LOADING
    ------------------------------------------------------------------------
    -->

    <div
      v-if="loading"
      class="team-loading"
    >
      Loading teams...
    </div>

    <!--
    ------------------------------------------------------------------------
    ERROR
    ------------------------------------------------------------------------
    -->

    <div
      v-else-if="error"
      class="team-error"
    >
      {{ error }}
    </div>

    <!--
    ------------------------------------------------------------------------
    TEAM LIST
    ------------------------------------------------------------------------
    -->

    <div
      v-else
      class="team-grid"
    >

      <div
        v-for="team in teams"
        :key="team.team_id"
        class="team-card"
      >

        <div
          class="team-color"
          :style="{
            backgroundColor:
              team.team_color
          }"
        />

        <h3>
          {{ team.team_name }}
        </h3>

      </div>

    </div>

  </section>

</template>

<style scoped>

.team-page {

  padding: 30px;
}

.team-page-header {

  margin-bottom: 30px;
}

.team-page-title {

  font-size: 32px;

  font-weight: 800;
}

.team-page-subtitle {

  margin-top: 6px;

  color: var(--text-muted);
}

.team-loading,
.team-error {

  padding: 30px;

  text-align: center;
}

.team-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;
}

.team-card {

  background-color: var(--white);

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  padding: 20px;
}

.team-color {

  width: 50px;

  height: 50px;

  border-radius: 50%;

  margin-bottom: 16px;
}

</style>