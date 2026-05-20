<script setup>

import { onMounted } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useGameStore

} from '../store/gameStore'


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
| GAME STORE
|--------------------------------------------------------------------------
*/

const gameStore =
  useGameStore()

const {

  games,

  loading,

  error

} = storeToRefs(
  gameStore
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
  LOAD EVENT GAMES
  --------------------------------------------------------------------------
  */

  await gameStore.loadGames()
})

</script>

<template>

  <section class="game-page">

    <!--
    ------------------------------------------------------------------------
    HEADER
    ------------------------------------------------------------------------
    -->

    <div class="game-page-header">

      <h1 class="game-page-title">

        {{ currentEvent?.event_name }}

      </h1>

      <p class="game-page-subtitle">

        Event Games

      </p>

    </div>

    <!--
    ------------------------------------------------------------------------
    LOADING
    ------------------------------------------------------------------------
    -->

    <div
      v-if="loading"
      class="game-loading"
    >
      Loading games...
    </div>

    <!--
    ------------------------------------------------------------------------
    ERROR
    ------------------------------------------------------------------------
    -->

    <div
      v-else-if="error"
      class="game-error"
    >
      {{ error }}
    </div>

    <!--
    ------------------------------------------------------------------------
    GAME LIST
    ------------------------------------------------------------------------
    -->

    <div
      v-else
      class="game-grid"
    >

      <div
        v-for="game in games"
        :key="game.game_id"
        class="game-card"
      >

        <h3>

          {{ game.sport_name }}

        </h3>

        <p>

          {{ game.round }}

        </p>

        <p>

          {{ game.game_status }}

        </p>

        <p>

          {{ game.venue_name }}

        </p>

      </div>

    </div>

  </section>

</template>

<style scoped>

.game-page {

  padding: 30px;
}

.game-page-header {

  margin-bottom: 30px;
}

.game-page-title {

  font-size: 32px;

  font-weight: 800;
}

.game-page-subtitle {

  margin-top: 6px;

  color: var(--text-muted);
}

.game-loading,
.game-error {

  padding: 30px;

  text-align: center;
}

.game-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(240px, 1fr));

  gap: 20px;
}

.game-card {

  background-color: var(--white);

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  padding: 20px;
}

</style>