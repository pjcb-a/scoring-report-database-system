<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import ScoringHeader from '../components/ScoringHeader.vue'
import MatchCard from '../components/MatchCard.vue'
import FinalizeMatchForm from '../components/FinalizeMatchForm.vue'
import { useScoringStore } from '../store/scoringStore'

const router = useRouter()
const eventContextStore = useEventContextStore()
const { currentEvent } = storeToRefs(eventContextStore)

const scoringStore = useScoringStore()
const {
  loading,
  pendingGames,
  finalizedGames
} = storeToRefs(scoringStore)

const { loadGames, finalizeGame } = scoringStore

const openModal = ref(false)
const selectedGame = ref(null)

const openFinalize = (game) => {
  selectedGame.value = game
  openModal.value = true
}

const closeModal = () => {
  openModal.value = false
  selectedGame.value = null
}

const handleFinalize = async (payload) => {
  if (!selectedGame.value) {
    return
  }

  await finalizeGame(selectedGame.value.game_id, payload)
  closeModal()
}

onMounted(async () => {
  if (!currentEvent.value) {
    router.push('/events')
    return
  }

  await loadGames()
})
</script>

<template>
  <div class="scoring-page">
    <div
      v-if="currentEvent"
      class="event-banner"
    >
      <span class="event-banner__label">Active Event</span>
      <strong>{{ currentEvent.event_name }}</strong>
    </div>

    <ScoringHeader />

    <LoadingSpinner v-if="loading" />

    <template v-else>
      <section class="scoring-section">
        <h2>Matches awaiting finalization</h2>

        <div
          v-if="!pendingGames.length"
          class="empty-state"
        >
          No pending matches. Create games under the Games tab first.
        </div>

        <div
          v-else
          class="match-grid"
        >
          <MatchCard
            v-for="game in pendingGames"
            :key="game.game_id"
            :game="game"
            @finalize="openFinalize(game)"
          />
        </div>
      </section>

      <section
        v-if="finalizedGames.length"
        class="scoring-section"
      >
        <h2>Recently finalized</h2>

        <div class="match-grid">
          <MatchCard
            v-for="game in finalizedGames"
            :key="`final-${game.game_id}`"
            :game="game"
            finalized
          />
        </div>
      </section>
    </template>

    <Modal
      :is-open="openModal"
      title="Finalize Match"
      @close="closeModal"
    >
      <FinalizeMatchForm
        v-if="selectedGame"
        :game="selectedGame"
        @submit="handleFinalize"
        @cancel="closeModal"
      />
    </Modal>
  </div>
</template>

<style scoped>
.scoring-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.event-banner {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px 18px;
  border-radius: 12px;
  background: var(--color-surface-alt, #f4f6fb);
  border: 1px solid var(--color-border, #e2e8f0);
}

.event-banner__label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-text-muted, #64748b);
}

.scoring-section h2 {
  margin: 0 0 14px;
  font-size: 1.1rem;
}

.match-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.25rem;
}

.empty-state {
  padding: 2rem;
  border-radius: 12px;
  background: white;
  text-align: center;
  color: var(--text-muted);
}
</style>
