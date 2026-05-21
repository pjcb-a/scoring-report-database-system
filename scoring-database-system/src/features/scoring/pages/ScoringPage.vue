<script setup>

import {
  computed,
  onMounted,
  ref,
  watch
} from 'vue'

import {
  storeToRefs
} from 'pinia'

import {
  useScoringStore
} from '../store/scoringStore'

import {
  useEventContextStore
} from '@/features/events/store/eventContextStore'

import ScoreForm from '../components/ScoreForm.vue'
import FinalizeMatchForm from '../components/FinalizeMatchForm.vue'

const scoringStore =
  useScoringStore()

const eventContextStore =
  useEventContextStore()

const {
  scores,
  loading,
  error
} = storeToRefs(scoringStore)

const currentEventId =
  computed(() => {

    return eventContextStore
      .currentEventId
  })

const showScoreModal =
  ref(false)

const showFinalizeModal =
  ref(false)

const selectedGame =
  ref(null)

/*
|--------------------------------------------------------------------------
| SAFE SCORES
|--------------------------------------------------------------------------
*/

const safeScores =
  computed(() => {

    return Array.isArray(scores.value)

      ? scores.value

      : []
  })

/*
|--------------------------------------------------------------------------
| GROUP SCORES BY GAME
|--------------------------------------------------------------------------
*/

const groupedScores =
  computed(() => {

    const grouped = {}

    safeScores.value.forEach(score => {

      const gameId =
        score.game_id

      if (!grouped[gameId]) {

        grouped[gameId] = {

          game_id:
            gameId,

          game_status:
            score.game_status,

          round:
            score.round,

          sport_name:
            score.sport_name,

          game_date:
            score.game_date,

          teams: []
        }
      }

      grouped[gameId]
        .teams
        .push({

          team_name:
            score.team_name,

          score_value:
            score.score_value
        })
    })

    return Object.values(grouped)
  })

/*
|--------------------------------------------------------------------------
| LOAD SCORES
|--------------------------------------------------------------------------
*/

const loadPage =
  async () => {

    if (!currentEventId.value) {
      return
    }

    await scoringStore.loadScores()
  }

onMounted(async () => {

  await loadPage()
})

watch(

  currentEventId,

  async () => {

    await loadPage()
  }
)

/*
|--------------------------------------------------------------------------
| MODAL ACTIONS
|--------------------------------------------------------------------------
*/

const openFinalizeModal =
  (game) => {

    selectedGame.value =
      game

    showFinalizeModal.value =
      true
  }

const closeFinalizeModal =
  () => {

    selectedGame.value =
      null

    showFinalizeModal.value =
      false
  }

const handleFinalizeSuccess =
  async () => {

    await scoringStore.loadScores()

    closeFinalizeModal()
  }

const closeScoreModal =
  () => {

    showScoreModal.value =
      false
  }

const handleScoreSuccess =
  async () => {

    await scoringStore.loadScores()

    closeScoreModal()
  }

</script>

<template>

  <section class="scoring-page">

    <div class="page-header">

      <div>

        <h1>
          Scoring
        </h1>

        <p>
          Manage event game scores
        </p>

      </div>

      <button
        class="primary-btn"
        @click="showScoreModal = true"
      >
        Add Score
      </button>

    </div>

    <!-- LOADING -->

    <div
      v-if="loading"
      class="loading-state"
    >
      Loading scores...
    </div>

    <!-- ERROR -->

    <div
      v-else-if="error"
      class="error-state"
    >
      {{ error }}
    </div>

    <!-- EMPTY -->

    <div
      v-else-if="groupedScores.length === 0"
      class="empty-state"
    >
      No scores available.
    </div>

    <!-- SCORE LIST -->

    <div
      v-else
      class="score-grid"
    >

      <div

        v-for="game in groupedScores"

        :key="game.game_id"

        class="score-card"
      >

        <div class="score-card-header">

          <div>

            <h3>
              {{ game.sport_name }}
            </h3>

            <p>
              {{ game.round }}
            </p>

          </div>

          <span class="status-badge">
            {{ game.game_status }}
          </span>

        </div>

        <div class="teams-list">

          <div

            v-for="team in game.teams"

            :key="team.team_name"

            class="team-row"
          >

            <span>
              {{ team.team_name }}
            </span>

            <strong>
              {{ team.score_value }}
            </strong>

          </div>

        </div>

        <div class="score-card-footer">

          <small>
            {{ game.game_date }}
          </small>

          <button

            class="secondary-btn"

            @click="openFinalizeModal(game)"
          >
            Finalize
          </button>

        </div>

      </div>

    </div>

    <!-- SCORE MODAL -->

    <div
      v-if="showScoreModal"
      class="modal-overlay"
    >

      <div class="modal-content">

        <ScoreForm

          :game-scores="safeScores"

          @success="handleScoreSuccess"

          @close="closeScoreModal"
        />

      </div>

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

  </section>

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
