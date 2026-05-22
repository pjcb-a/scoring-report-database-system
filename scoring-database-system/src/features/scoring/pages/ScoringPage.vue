<script setup>
import { computed, onMounted, ref, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { getGamesByEvent } from '@/features/games/services/gameService'
import { isFinalizedGame, isScheduledGame } from '@/utils/gameLifecycle'
import { useGameStore } from '@/features/games/store/gameStore'
import MatchCard from '../components/MatchCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import FinalizeMatchForm from '../components/FinalizeMatchForm.vue'

const eventContextStore = useEventContextStore()
const gameStore = useGameStore()
const { currentEventId } = storeToRefs(eventContextStore)

const games = ref([])
const loading = ref(false)
const error = ref(null)
const showFinalizeModal = ref(false)
const selectedGame = ref(null)

const isComponentGame = (game) =>
  game.scoring_type === 'Component Score'

const nonComponentGames = computed(() =>
  games.value.filter(game => !isComponentGame(game))
)

const pendingGames = computed(() =>
  nonComponentGames.value.filter(isScheduledGame)
)

const finalizedGames = computed(() =>
  nonComponentGames.value.filter(isFinalizedGame)
)

const loadGames = async () => {
  if (!currentEventId.value) {
    games.value = []
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await getGamesByEvent(currentEventId.value)
    games.value = response?.data || []
  } catch (err) {
    console.error('Error loading games:', err)
    error.value = err.message || 'Failed to load games.'
    games.value = []
  } finally {
    loading.value = false
  }
}

const openFinalize = (game) => {
  selectedGame.value = game
  showFinalizeModal.value = true
}

const closeFinalizeModal = () => {
  selectedGame.value = null
  showFinalizeModal.value = false
}

const handleFinalizeSuccess = async () => {
  await loadGames()
  await gameStore.loadGames()
  closeFinalizeModal()
}

onMounted(async () => {
  await nextTick()
  setTimeout(() => {
    loadGames()
  }, 100)
})
</script>

<template>
  <div class="scoring-page">
    <div class="scoring-header">
      <h1>Scoring</h1>
      <p>Manage and finalize non-component score matches</p>
    </div>

    <LoadingSpinner v-if="loading" />

    <div
      v-else-if="error"
      class="error-state"
    >
      {{ error }}
    </div>

    <div
      v-else
      class="scoring-body"
    >
      <section class="scoring-section">
        <header class="scoring-section__header">
          <h2>Matches awaiting finalization</h2>
          <p class="scoring-section__hint">
            Enter scores and mark a winner to finalize each match.
          </p>
        </header>

        <div
          v-if="!pendingGames.length"
          class="empty-state"
        >
          No pending matches. Create games for non-component score sports under the Games tab.
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
        class="scoring-section scoring-section--finalized"
      >
        <header class="scoring-section__header">
          <h2>Recently finalized</h2>
          <p class="scoring-section__hint">
            Concluded matches with outcome and scores on record.
          </p>
        </header>

        <div class="match-grid">
          <MatchCard
            v-for="game in finalizedGames"
            :key="`final-${game.game_id}`"
            :game="game"
            finalized
          />
        </div>
      </section>
    </div>

    <!-- FINALIZE MODAL -->
    <div
      v-if="showFinalizeModal"
      class="modal-overlay"
    >
      <div class="modal-content">
        <FinalizeMatchForm
          v-if="selectedGame"
          :game="selectedGame"
          @success="handleFinalizeSuccess"
          @close="closeFinalizeModal"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.scoring-page {
  display: flex;
  flex-direction: column;
  gap: 0;
  max-width: 1200px;
}

.scoring-header {
  margin-bottom: 28px;
}

.scoring-header h1 {
  margin: 0 0 8px;
  font-size: 1.75rem;
}

.scoring-header p {
  margin: 0;
  color: var(--text-muted, #64748b);
  line-height: 1.5;
}

.scoring-body {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.scoring-section {
  margin: 0;
}

.scoring-section--finalized {
  padding-top: 32px;
  border-top: 1px solid var(--border-color, #e2e8f0);
}

.scoring-section__header {
  margin: 0 0 20px;
}

.scoring-section__header h2 {
  margin: 0 0 6px;
  font-size: 1.15rem;
  font-weight: 700;
}

.scoring-section__hint {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-muted, #64748b);
  line-height: 1.45;
}

.match-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.empty-state {
  margin: 0;
  padding: 28px 24px;
  border-radius: 12px;
  background: white;
  text-align: center;
  color: var(--text-muted);
  line-height: 1.5;
  border: 1px solid var(--border-color, #e2e8f0);
}

.error-state {
  padding: 1.5rem;
  border-radius: 12px;
  background: #fee2e2;
  color: #b91c1c;
  font-weight: 600;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 680px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}
</style>
