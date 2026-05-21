<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import JudgingHeader from '../components/JudgingHeader.vue'
import JudgingSetupPanel from '../components/JudgingSetupPanel.vue'
import MatchCard from '@/features/scoring/components/MatchCard.vue'
import JudgingFinalizeMatchForm from '../components/JudgingFinalizeMatchForm.vue'
import { useJudgingStore } from '../store/judgingStore'

const router = useRouter()
const eventContextStore = useEventContextStore()
const { currentEvent } = storeToRefs(eventContextStore)

const judgingStore = useJudgingStore()
const {
  loading,
  pendingGames,
  finalizedGames,
  judges
} = storeToRefs(judgingStore)

const { loadGames, loadJudges, finalizeGame } = judgingStore

const openModal = ref(false)
const selectedGame = ref(null)

const openFinalize = async (game) => {
  await loadJudges()
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

  await Promise.all([loadGames(), loadJudges()])
})
</script>

<template>
  <div class="judging-page">
    <div
      v-if="currentEvent"
      class="event-banner"
    >
      <span class="event-banner__label">Active Event</span>
      <strong>{{ currentEvent.event_name }}</strong>
    </div>

    <JudgingHeader />

    <JudgingSetupPanel />

    <LoadingSpinner v-if="loading" />

    <template v-else>
      <section class="judging-section">
        <h2>Component-score matches awaiting finalization</h2>

        <div
          v-if="!pendingGames.length"
          class="empty-state"
        >
          No pending component-score matches. Create games for a Component Score sport under the Games tab.
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
        class="judging-section"
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
      title="Finalize Component-Score Match"
      @close="closeModal"
    >
      <JudgingFinalizeMatchForm
        v-if="selectedGame"
        :game="selectedGame"
        :judges="judges"
        @submit="handleFinalize"
        @cancel="closeModal"
      />
    </Modal>
  </div>
</template>

<style scoped>
.judging-page {
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

.judging-section h2 {
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
