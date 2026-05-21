<script setup>

import { onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useSportStore

} from '../store/sportStore'

import SportForm from '../components/SportForm.vue'


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
| STATE
|--------------------------------------------------------------------------
*/

const showSportForm = ref(false)


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

      <div>
        <h1>
          {{ currentEvent?.event_name }}
        </h1>

        <p>
          Manage event sports.
        </p>
      </div>

      <button

        class="add-sport-btn"

        @click="showSportForm = true"
      >
        <i class="fa-solid fa-plus"></i>

        Add Sport
      </button>

    </div>

    <!--
    ------------------------------------------------------------------------
    SPORT FORM
    ------------------------------------------------------------------------
    -->

    <SportForm

      v-if="showSportForm"

      @close="showSportForm = false"

      @success="showSportForm = false"
    />

    <!--
    ------------------------------------------------------------------------
    LOADING
    ------------------------------------------------------------------------
    -->

    <div
      v-if="loading"
      class="loading-state"
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
      v-else-if="!sports.length"
      class="empty-state"
    >
      No sports found. Add your first sport.
    </div>

    <div
      v-else
      class="sport-grid"
    >

      <div
        v-for="sport in sports"
        :key="sport.event_sport_id"
        class="sport-card"
      >

        <div class="sport-card-header">

          <h3>
            {{ sport.sport_name }}
          </h3>

          <div class="sport-badge">
            {{ sport.scoring_type }}
          </div>

        </div>

      </div>

    </div>

  </section>

</template>

<style scoped>

.sport-page {

  display: flex;

  flex-direction: column;

  gap: 1.5rem;
}

.sport-page-header {

  display: flex;

  align-items: center;

  justify-content: space-between;
}

.sport-page-header h1 {

  font-size: 32px;

  font-weight: 800;
}

.sport-page-header p {

  margin-top: 6px;

  color: var(--text-muted);
}

.add-sport-btn {

  display: flex;

  align-items: center;

  gap: 0.6rem;

  padding: 0.8rem 1rem;

  border: none;

  border-radius: 10px;

  background: #2563eb;

  color: white;

  cursor: pointer;

  font-weight: 600;

  transition: 0.2s ease;
}

.add-sport-btn:hover {

  background: #1d4ed8;
}

.loading-state,
.empty-state {

  padding: 2rem;

  border-radius: 12px;

  background: white;

  text-align: center;

  color: var(--text-muted);
}

.sport-error {

  padding: 30px;

  text-align: center;
}

.sport-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(260px, 1fr));

  gap: 1.25rem;
}

.sport-card {

  background-color: white;

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  padding: 1.25rem;

  transition: 0.2s ease;
}

.sport-card:hover {

  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.08);

  transform: translateY(-1px);
}

.sport-card-header {

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 0.75rem;
}

.sport-card-header h3 {

  font-size: 1.05rem;

  font-weight: 700;

  margin: 0;
}

.sport-badge {

  padding: 0.3rem 0.7rem;

  border-radius: 999px;

  background: #dbeafe;

  color: #1d4ed8;

  font-size: 0.75rem;

  font-weight: 600;

  white-space: nowrap;
}

</style>