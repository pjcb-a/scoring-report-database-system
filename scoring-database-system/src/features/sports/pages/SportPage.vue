<script setup>

import { onMounted } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useSportStore

} from '../store/sportStore'


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
| SPORT STORE
|--------------------------------------------------------------------------
*/

const sportStore =
  useSportStore()

const {

  sports,

  loading,

  error

} = storeToRefs(
  sportStore
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
  LOAD EVENT SPORTS
  --------------------------------------------------------------------------
  */

  await sportStore.loadSports()
})

</script>

<template>

  <section class="sport-page">

    <!--
    ------------------------------------------------------------------------
    HEADER
    ------------------------------------------------------------------------
    -->

    <div class="sport-page-header">

      <h1 class="sport-page-title">

        {{ currentEvent?.event_name }}

      </h1>

      <p class="sport-page-subtitle">

        Event Sports

      </p>

    </div>

    <!--
    ------------------------------------------------------------------------
    LOADING
    ------------------------------------------------------------------------
    -->

    <div
      v-if="loading"
      class="sport-loading"
    >
      Loading sports...
    </div>

    <!--
    ------------------------------------------------------------------------
    ERROR
    ------------------------------------------------------------------------
    -->

    <div
      v-else-if="error"
      class="sport-error"
    >
      {{ error }}
    </div>

    <!--
    ------------------------------------------------------------------------
    SPORT LIST
    ------------------------------------------------------------------------
    -->

    <div
      v-else
      class="sport-grid"
    >

      <div
        v-for="sport in sports"
        :key="sport.event_sport_id"
        class="sport-card"
      >

        <h3>

          {{ sport.sport_name }}

        </h3>

        <p>

          {{ sport.scoring_type }}

        </p>

      </div>

    </div>

  </section>

</template>

<style scoped>

.sport-page {

  padding: 30px;
}

.sport-page-header {

  margin-bottom: 30px;
}

.sport-page-title {

  font-size: 32px;

  font-weight: 800;
}

.sport-page-subtitle {

  margin-top: 6px;

  color: var(--text-muted);
}

.sport-loading,
.sport-error {

  padding: 30px;

  text-align: center;
}

.sport-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;
}

.sport-card {

  background-color: var(--white);

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  padding: 20px;
}

</style>