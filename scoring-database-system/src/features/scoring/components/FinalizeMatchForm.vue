<script setup>
import { computed, reactive, watch } from 'vue'
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import { THRESHOLD_INCREMENTAL } from '../store/scoringStore'

const props = defineProps({
  game: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['submit', 'cancel'])

const GAME_STATUS_OPTIONS = [
  'Win',
  'Forfeit',
  'Suspensions'
]

const form = reactive({
  game_status: 'Win',
  winner_team_id: '',
  teams: []
})

const isThreshold = computed(() =>
  props.game.scoring_type === THRESHOLD_INCREMENTAL
)

const isRankedTimed = computed(() =>
  props.game.scoring_type === 'Ranked Timed'
)

const setCount = computed(() =>
  Number(props.game.set_count) || 0
)

const buildTeamEntry = (team) => {
  const base = {
    team_id: team.team_id,
    team_name: team.team_name,
    team_color: team.team_color,
    total_score: '',
    rank_position: '',
    sets_won: '',
    set_scores: []
  }

  if (isThreshold.value && setCount.value > 0) {
    base.set_scores = Array.from(
      { length: setCount.value },
      () => ''
    )
  }

  return base
}

const initForm = () => {
  const teams = props.game.teams || []

  form.game_status = 'Win'
  form.winner_team_id = ''
  form.teams = teams.map(team => buildTeamEntry(team))
}

watch(
  () => props.game?.game_id,
  () => initForm(),
  { immediate: true }
)

const submitForm = () => {
  if (!form.game_status) {
    return
  }

  const teamsPayload = form.teams.map(entry => {
    const payload = {
      team_id: entry.team_id,
      is_winner: Number(form.winner_team_id) === Number(entry.team_id)
    }

    if (isThreshold.value) {
      payload.set_scores = entry.set_scores.map(value => Number(value))
      payload.sets_won = Number(entry.sets_won)
    } else {
      payload.total_score = Number(entry.total_score)

      if (isRankedTimed.value && entry.rank_position !== '') {
        payload.rank_position = Number(entry.rank_position)
      }
    }

    return payload
  })

  for (const entry of teamsPayload) {
    if (isThreshold.value) {
      if (
        entry.set_scores.some(value => Number.isNaN(value))
        || Number.isNaN(entry.sets_won)
      ) {
        return
      }
    } else if (Number.isNaN(entry.total_score)) {
      return
    }
  }

  emit('submit', {
    game_status: form.game_status,
    teams: teamsPayload
  })
}
</script>

<template>
  <form
    class="finalize-form"
    @submit.prevent="submitForm"
  >
    <div class="match-summary">
      <h3>{{ game.sport || game.game_name }}</h3>
      <p v-if="game.round">
        {{ game.round }}
      </p>
      <p class="match-meta">
        {{ game.scoring_type }}
        <span v-if="isThreshold">
          · {{ setCount }} sets
        </span>
      </p>
    </div>

    <div class="input-group">
      <label class="form-label">
        How did the match conclude?
      </label>
      <select
        v-model="form.game_status"
        class="base-input"
      >
        <option
          v-for="status in GAME_STATUS_OPTIONS"
          :key="status"
          :value="status"
        >
          {{ status }}
        </option>
      </select>
    </div>

    <div
      v-for="entry in form.teams"
      :key="entry.team_id"
      class="team-score-block"
    >
      <div class="team-score-header">
        <span
          class="team-dot"
          :style="{ backgroundColor: entry.team_color }"
        />
        <strong>{{ entry.team_name }}</strong>
      </div>

      <template v-if="isThreshold">
        <div class="set-scores-grid">
          <Input
            v-for="(_, setIndex) in entry.set_scores"
            :key="`${entry.team_id}-set-${setIndex}`"
            v-model="entry.set_scores[setIndex]"
            :label="`Set ${setIndex + 1} score`"
            type="number"
            min="0"
            placeholder="0"
          />
        </div>

        <Input
          v-model="entry.sets_won"
          label="Sets won"
          type="number"
          min="0"
          :max="setCount"
          placeholder="0"
        />
      </template>

      <template v-else>
        <Input
          v-model="entry.total_score"
          label="Final score"
          type="number"
          min="0"
          placeholder="Enter score"
        />

        <Input
          v-if="isRankedTimed"
          v-model="entry.rank_position"
          label="Rank position"
          type="number"
          min="1"
          placeholder="Enter rank"
        />
      </template>

      <label class="winner-option">
        <input
          v-model="form.winner_team_id"
          type="radio"
          name="winner"
          :value="entry.team_id"
        >
        Mark as winner
      </label>
    </div>

    <div class="form-actions">
      <button
        type="button"
        class="cancel-btn"
        @click="emit('cancel')"
      >
        Cancel
      </button>

      <PrimaryButton>
        Finalize Match
      </PrimaryButton>
    </div>
  </form>
</template>

<style scoped>
.finalize-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.match-summary h3 {
  margin: 0;
  font-size: 1.15rem;
}

.match-summary p {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
}

.match-meta {
  font-size: 0.9rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 700;
}

.team-score-block {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.team-score-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.team-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.set-scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.winner-option {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 12px 18px;
  border: none;
  border-radius: var(--radius-md, 8px);
  background: #e5e7eb;
  color: #374151;
  font-weight: 700;
  cursor: pointer;
}
</style>
