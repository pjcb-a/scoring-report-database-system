<script setup>

import { onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useGameStore

} from '../store/gameStore'

import GameForm from '../components/GameForm.vue'

import GameCard from '../components/GameCard.vue'


const router = useRouter()

const eventContextStore =
  useEventContextStore()

const {

  currentEvent

} = storeToRefs(
  eventContextStore
)

const gameStore =
  useGameStore()

const {

  games,

  loading,

  error

} = storeToRefs(
  gameStore
)

const showGameForm = ref(false)

onMounted(async () => {

  if (!currentEvent.value) {

    router.push('/events')

    return
  }

  await gameStore.loadGames()
})

</script>

<template>

  <section class="game-page">

    <div class="game-page-header">

      <div>
        <h1>
          {{ currentEvent?.event_name }}
        </h1>

        <p>
          Manage event games.
        </p>
      </div>

      <button
        class="add-game-btn"
        @click="showGameForm = true"
      >
        <i class="fa-solid fa-plus"></i>

        Create Game
      </button>

    </div>

    <GameForm
      v-if="showGameForm"
      @close="showGameForm = false"
      @success="showGameForm = false"
    />

    <div
      v-if="loading"
      class="loading-state"
    >
      Loading games...
    </div>

    <div
      v-else-if="error"
      class="game-error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="!games.length"
      class="empty-state"
    >
      No games found. Create your first game.
    </div>

    <div
      v-else
      class="game-grid"
    >

      <GameCard
        v-for="game in games"
        :key="game.game_id"
        :game="game"
      />

    </div>

  </section>

</template>

<style scoped>

.game-page {

  display: flex;

  flex-direction: column;

  gap: 1.5rem;
}

.game-page-header {

  display: flex;

  align-items: center;

  justify-content: space-between;
}

.game-page-header h1 {

  font-size: 32px;

  font-weight: 800;
}

.game-page-header p {

  margin-top: 6px;

  color: var(--text-muted);
}

.add-game-btn {

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

.add-game-btn:hover {

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

.game-error {

  padding: 2rem;

  border-radius: 12px;

  background: white;

  text-align: center;

  color: var(--adnu-danger);
}

.game-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(280px, 1fr));

  gap: 1.25rem;
}

</style>
