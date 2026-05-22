<script setup>
import { computed, reactive, ref, watch } from 'vue'
import Input from '@/components/ui/Input.vue'
import Badge from '@/components/ui/Badge.vue'
import { useScoringStore } from '../store/scoringStore'

const THRESHOLD_INCREMENTAL = 'Threshold Incremental'
const RANKED_TIMED = 'Ranked Timed'

const props = defineProps({
  game: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['success', 'close'])

const scoringStore = useScoringStore()
const saving = ref(false)
const formError = ref('')

const GAME_STATUS_OPTIONS = ['Win', 'Forfeit', 'Suspensions']

const form = reactive({
  game_status: 'Win',
  winner_team_id: '',
  teams: []
})

const scoringType = computed(
  () => props.game.scoring_type || ''
)

const isThreshold = computed(
  () => scoringType.value === THRESHOLD_INCREMENTAL
)

const isRankedTimed = computed(
  () => scoringType.value === RANKED_TIMED
)

const setCount = computed(
  () => Number(props.game.set_count) || 0
)

const gameTitle = computed(() => {
  const teams = props.game.teams || []

  if (teams.length >= 2) {
    return `${teams[0].team_name} vs ${teams[1].team_name}`
  }

  if (teams.length === 1) {
    return teams[0].team_name
  }

  return props.game.sport || props.game.game_name || 'Match'
})

const buildTeamEntry = (team) => {
  const entry = {
    team_id: team.team_id,
    team_name: team.team_name,
    team_color: team.team_color,
    total_score: '',
    rank_position: '',
    sets_won: '',
    set_scores: []
  }

  if (isThreshold.value && setCount.value > 0) {
    entry.set_scores = Array.from(
      { length: setCount.value },
      () => ''
    )
  }

  return entry
}

const initForm = () => {
  form.game_status = 'Win'
  form.winner_team_id = ''
  form.teams = (props.game.teams || []).map(team =>
    buildTeamEntry(team)
  )
  formError.value = ''
}

watch(
  () => props.game?.game_id,
  () => initForm(),
  { immediate: true }
)

const selectWinner = (teamId) => {
  form.winner_team_id = teamId
}

const buildTeamsPayload = () =>
  form.teams.map(entry => {
    const payload = {
      team_id: entry.team_id,
      is_winner:
        Number(form.winner_team_id) === Number(entry.team_id)
    }

    if (isThreshold.value) {
      payload.set_scores = entry.set_scores.map(value =>
        Number(value)
      )
      payload.sets_won = Number(entry.sets_won)
    } else {
      payload.total_score = Number(entry.total_score)

      if (isRankedTimed.value && entry.rank_position !== '') {
        payload.rank_position = Number(entry.rank_position)
      }
    }

    return payload
  })

const validateForm = () => {
  if (!form.game_status) {
    formError.value = 'Select how the match concluded.'
    return false
  }

  if (!form.teams.length) {
    formError.value = 'This match has no teams to score.'
    return false
  }

  for (const entry of form.teams) {
    if (isThreshold.value) {
      if (
        entry.set_scores.some(value => value === '' || Number.isNaN(Number(value)))
        || entry.sets_won === ''
        || Number.isNaN(Number(entry.sets_won))
      ) {
        formError.value = 'Enter all set scores and sets won for each team.'
        return false
      }
    } else if (
      entry.total_score === ''
      || Number.isNaN(Number(entry.total_score))
    ) {
      formError.value = 'Enter a score for each team.'
      return false
    }

    if (
      isRankedTimed.value
      && entry.rank_position !== ''
      && Number(entry.rank_position) <= 0
    ) {
      formError.value = 'Rank position must be at least 1.'
      return false
    }
  }

  formError.value = ''
  return true
}

const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  saving.value = true

  try {
    await scoringStore.finalizeGame(props.game.game_id, {
      game_status: form.game_status,
      teams: buildTeamsPayload()
    })

    emit('success')
    emit('close')
  } catch (err) {
    console.error(err)
    formError.value =
      err.message || 'Failed to finalize match.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form
    class="finalize-form"
    @submit.prevent="submitForm"
  >
    <div class="form-header">
      <h2>Finalize Match</h2>
      <p class="game-title">
        {{ gameTitle }}
      </p>
      <p class="game-meta">
        {{ scoringType }}
        <span v-if="isThreshold && setCount">
          · {{ setCount }} sets
        </span>
      </p>
    </div>

    <div class="form-group">
      <label class="form-label">
        How did the match conclude?
      </label>
      <select
        v-model="form.game_status"
        class="form-select"
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

    <section class="teams-section">
      <h3 class="section-title">
        Team scores
      </h3>
      <p class="section-hint">
        Enter scores for every team, then mark the winner.
      </p>

      <div
        v-for="entry in form.teams"
        :key="entry.team_id"
        class="team-score-block"
        :class="{
          'team-score-block--winner':
            Number(form.winner_team_id) === Number(entry.team_id)
        }"
      >
        <div class="team-score-header">
          <div class="team-identity">
            <span
              class="team-dot"
              :style="{ backgroundColor: entry.team_color }"
            />
            <strong>{{ entry.team_name }}</strong>
            <Badge
              v-if="Number(form.winner_team_id) === Number(entry.team_id)"
              label="Winner"
              variant="success"
            />
          </div>
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

        <button
          type="button"
          class="winner-toggle"
          :class="{
            'winner-toggle--active':
              Number(form.winner_team_id) === Number(entry.team_id)
          }"
          @click="selectWinner(entry.team_id)"
        >
          {{
            Number(form.winner_team_id) === Number(entry.team_id)
              ? 'Marked as winner'
              : 'Mark as winner'
          }}
        </button>
      </div>
    </section>

    <p
      v-if="formError"
      class="form-error"
    >
      {{ formError }}
    </p>

    <div class="form-actions">
      <button
        type="button"
        class="cancel-btn"
        @click="emit('close')"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="save-btn"
        :disabled="saving"
      >
        <i
          v-if="saving"
          class="fa-solid fa-spinner fa-spin"
        />
        <i
          v-else
          class="fa-solid fa-check"
        />
        {{ saving ? 'Finalizing...' : 'Finalize Match' }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.finalize-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-header h2 {
  margin: 0 0 6px;
  font-size: 1.25rem;
}

.game-title {
  margin: 0;
  font-weight: 600;
}

.game-meta {
  margin: 4px 0 0;
  font-size: 0.9rem;
  color: var(--text-muted, #64748b);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 700;
}

.form-select {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: white;
}

.teams-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  margin: 0;
  font-size: 1rem;
}

.section-hint {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
}

.team-score-block {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 14px;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.team-score-block--winner {
  border-color: #86efac;
  background: #f0fdf4;
  box-shadow: 0 0 0 1px #bbf7d0;
}

.team-score-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.team-identity {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.team-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
}

.set-scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.winner-toggle {
  align-self: flex-start;
  padding: 8px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-weight: 600;
  cursor: pointer;
  transition: 0.15s ease;
}

.winner-toggle--active {
  border-color: #16a34a;
  background: #dcfce7;
  color: #166534;
}

.form-error {
  margin: 0;
  color: #b91c1c;
  font-size: 0.9rem;
  font-weight: 600;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn,
.save-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
}

.cancel-btn {
  background: #e5e7eb;
  color: #374151;
}

.save-btn {
  background: #2563eb;
  color: white;
}

.save-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
