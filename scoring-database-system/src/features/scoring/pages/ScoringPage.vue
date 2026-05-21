<script setup>
import { computed, onMounted, ref, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { getGamesByEvent } from '@/features/games/services/gameService'
import MatchCard from '../components/MatchCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import FinalizeMatchForm from '../components/FinalizeMatchForm.vue'

const eventContextStore = useEventContextStore()
const { currentEvent, currentEventId } = storeToRefs(eventContextStore)

const games = ref([])
const loading = ref(false)
const error = ref(null)
const showFinalizeModal = ref(false)
const selectedGame = ref(null)

// Filter for non-component score games
const nonComponentGames = computed(() => {
  return games.value.filter(game => {
    const scoringType = game.sport?.scoring_type || game.scoring_type || ''
    return scoringType.toLowerCase() !== 'component' && 
           scoringType !== 'Component Score'
  })
})

const pendingGames = computed(() => {
  return nonComponentGames.value.filter(game => game.status !== 'finalized')
})

const finalizedGames = computed(() => {
  return nonComponentGames.value.filter(game => game.status === 'finalized')
})

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
    console.log('Loaded games:', games.value)
    console.log('Non-component games:', nonComponentGames.value)
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
    <div
      v-if="currentEvent"
      class="event-banner"
    >
      <span class="event-banner__label">Active Event</span>
      <strong>{{ currentEvent.event_name }}</strong>
    </div>

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

    <template v-else>
      <section class="scoring-section">
        <h2>Matches awaiting finalization</h2>

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

.scoring-header h1 {
  margin: 0 0 0.5rem;
  font-size: 1.75rem;
}

.scoring-header p {
  margin: 0;
  color: var(--text-muted, #64748b);
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
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}
</style>
