<script setup>
import { computed, reactive, ref, watch } from 'vue'
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import { getCriteriaByEventSport } from '@/features/sports/services/criteriaService'

const props = defineProps({
  game: {
    type: Object,
    required: true
  },
  judges: {
    type: Array,
    default: () => []
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

const criteriaList = ref([])
const criteriaLoading = ref(false)
const criteriaError = ref('')

const buildScoreGrid = () => {
  const grid = {}

  for (const judge of props.judges) {
    grid[judge.judge_id] = {}

    for (const criterion of criteriaList.value) {
      grid[judge.judge_id][criterion.criteria_id] = ''
    }
  }

  return grid
}

const buildTeamEntry = (team) => ({
  team_id: team.team_id,
  team_name: team.team_name,
  team_color: team.team_color,
  judge_scores: buildScoreGrid()
})

const initForm = () => {
  form.game_status = 'Win'
  form.winner_team_id = ''
  form.teams = (props.game.teams || []).map(team => buildTeamEntry(team))
}

const loadCriteria = async () => {
  if (!props.game.event_sport_id) {
    criteriaList.value = []
    return
  }

  criteriaLoading.value = true
  criteriaError.value = ''

  try {
    const response = await getCriteriaByEventSport(
      props.game.event_sport_id
    )
    criteriaList.value = response.data || []

    if (!criteriaList.value.length) {
      criteriaError.value =
        'No criteria for this sport. Add criteria in the setup section above.'
    }

    initForm()
  } catch (err) {
    console.error(err)
    criteriaError.value = 'Failed to load criteria.'
  } finally {
    criteriaLoading.value = false
  }
}

const canSubmit = computed(() =>
  criteriaList.value.length > 0
  && props.judges.length > 0
  && !criteriaLoading.value
)

watch(
  () => [props.game?.game_id, props.judges.length],
  () => {
    initForm()
    loadCriteria()
  },
  { immediate: true }
)

const submitForm = () => {
  if (!canSubmit.value) {
    return
  }

  const teamsPayload = form.teams.map(entry => {
    const judge_scores = []

    for (const judge of props.judges) {
      for (const criterion of criteriaList.value) {
        const value = Number(
          entry.judge_scores[judge.judge_id][criterion.criteria_id]
        )

        if (Number.isNaN(value)) {
          return null
        }

        judge_scores.push({
          judge_id: judge.judge_id,
          criteria_id: criterion.criteria_id,
          score_value: value
        })
      }
    }

    if (!judge_scores) {
      return null
    }

    return {
      team_id: entry.team_id,
      is_winner: Number(form.winner_team_id) === Number(entry.team_id),
      judge_scores
    }
  })

  if (teamsPayload.some(team => !team)) {
    return
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
        Component Score · {{ judges.length }} judge(s) · {{ criteriaList.length }} criteria
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

    <p
      v-if="!judges.length"
      class="form-error"
    >
      Add at least one judge in the setup section before finalizing.
    </p>

    <p
      v-else-if="criteriaLoading"
      class="form-hint"
    >
      Loading criteria...
    </p>

    <p
      v-else-if="criteriaError"
      class="form-error"
    >
      {{ criteriaError }}
    </p>

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

      <div
        v-for="judge in judges"
        :key="`${entry.team_id}-${judge.judge_id}`"
        class="judge-block"
      >
        <h4>{{ judge.judge_name }}</h4>

        <div class="criteria-grid">
          <Input
            v-for="criterion in criteriaList"
            :key="`${entry.team_id}-${judge.judge_id}-${criterion.criteria_id}`"
            v-model="entry.judge_scores[judge.judge_id][criterion.criteria_id]"
            :label="`${criterion.criteria_name} (${criterion.percentage}%)`"
            type="number"
            min="0"
            placeholder="Score"
          />
        </div>
      </div>

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

      <PrimaryButton :disabled="!canSubmit">
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
  max-height: 70vh;
  overflow-y: auto;
}

.match-summary h3 {
  margin: 0;
}

.match-meta {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
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

.form-hint {
  margin: 0;
  color: var(--text-muted);
}

.form-error {
  margin: 0;
  color: #b91c1c;
  font-weight: 600;
}

.team-score-block {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
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

.judge-block h4 {
  margin: 0 0 8px;
  font-size: 0.95rem;
}

.criteria-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
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
  border-radius: 8px;
  background: #e5e7eb;
  font-weight: 700;
  cursor: pointer;
}
</style>
