<script setup>

import { onMounted } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useReportStore

} from '../store/reportStore'


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
| REPORT STORE
|--------------------------------------------------------------------------
*/

const reportStore =
  useReportStore()

const {

  rankings,

  loading,

  error

} = storeToRefs(
  reportStore
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
  LOAD EVENT REPORTS
  --------------------------------------------------------------------------
  */

  await reportStore.loadRankings()
})

</script>

<template>

  <section class="reports-page">

    <!--
    ------------------------------------------------------------------------
    HEADER
    ------------------------------------------------------------------------
    -->

    <div class="reports-header">

      <h1 class="reports-title">

        {{ currentEvent?.event_name }}

      </h1>

      <p class="reports-subtitle">

        Event Rankings & Reports

      </p>

    </div>

    <!--
    ------------------------------------------------------------------------
    LOADING
    ------------------------------------------------------------------------
    -->

    <div
      v-if="loading"
      class="reports-loading"
    >
      Loading reports...
    </div>

    <!--
    ------------------------------------------------------------------------
    ERROR
    ------------------------------------------------------------------------
    -->

    <div
      v-else-if="error"
      class="reports-error"
    >
      {{ error }}
    </div>

    <!--
    ------------------------------------------------------------------------
    RANKINGS
    ------------------------------------------------------------------------
    -->

    <div
      v-else
      class="rankings-table-wrapper"
    >

      <table class="rankings-table">

        <thead>

          <tr>

            <th>Rank</th>

            <th>Team</th>

            <th>Total Score</th>

          </tr>

        </thead>

        <tbody>

          <tr
            v-for="(
              ranking,
              index
            ) in rankings"

            :key="ranking.team_id"
          >

            <td>

              #{{ index + 1 }}

            </td>

            <td>

              <div class="team-cell">

                <div
                  class="team-color"
                  :style="{
                    backgroundColor:
                      ranking.team_color
                  }"
                />

                {{ ranking.team_name }}

              </div>

            </td>

            <td>

              {{ ranking.total_score }}

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </section>

</template>

<style scoped>

.reports-page {

  padding: 30px;
}

.reports-header {

  margin-bottom: 30px;
}

.reports-title {

  font-size: 32px;

  font-weight: 800;
}

.reports-subtitle {

  margin-top: 6px;

  color: var(--text-muted);
}

.reports-loading,
.reports-error {

  padding: 30px;

  text-align: center;
}

.rankings-table-wrapper {

  overflow-x: auto;
}

.rankings-table {

  width: 100%;

  border-collapse: collapse;

  background-color: var(--white);

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  overflow: hidden;
}

.rankings-table th,
.rankings-table td {

  padding: 16px;

  text-align: left;

  border-bottom:
    1px solid var(--border-color);
}

.team-cell {

  display: flex;

  align-items: center;

  gap: 12px;
}

.team-color {

  width: 18px;

  height: 18px;

  border-radius: 50%;
}

</style>