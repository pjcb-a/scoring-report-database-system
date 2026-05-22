<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import { required } from '@/utils/validators'
import { createValidation } from '@/utils/validation'
import { useGameStore } from '../store/gameStore'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { getTeamsByEvent } from '@/features/teams/services/teamService'

const props = defineProps({
  game: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['success', 'close'])

const gameStore = useGameStore()
const eventContextStore = useEventContextStore()

const gameName = ref('')
const startTime = ref('')
const endTime = ref('')
const venue = ref('')
const setCount = ref('')
const round = ref('')
const selectedTeamIds = ref([])
const saving = ref(false)
const eventTeams = ref([])

const isThresholdIncremental = computed(
  () => props.game.scoring_type === 'Threshold Incremental'
)

const { errors, setError, clearErrors, hasErrors } = createValidation()

const toDatetimeLocal = (value) => {
  if (!value) {
    return ''
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return ''
  }

  const pad = (n) => String(n).padStart(2, '0')

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

const populateForm = () => {
  gameName.value = props.game.game_name || ''
  startTime.value = toDatetimeLocal(props.game.start_date)
  endTime.value = toDatetimeLocal(props.game.end_date)
  venue.value = props.game.venue_name || ''
  setCount.value = props.game.set_count ? String(props.game.set_count) : ''
  round.value = props.game.round || ''
  selectedTeamIds.value = (props.game.teams || []).map(
    team => team.team_id
  )
}

const loadTeams = async () => {
  if (!eventContextStore.currentEventId) {
    return
  }

  try {
    const response = await getTeamsByEvent(
      eventContextStore.currentEventId
    )
    eventTeams.value = response?.data || []
  } catch (err) {
    console.error(err)
  }
}

onMounted(async () => {
  populateForm()
  await loadTeams()
})

watch(
  () => props.game?.game_id,
  () => populateForm()
)

const submitGame = async () => {
  if (saving.value) {
    return
  }

  clearErrors()

  const nameError = required(gameName.value.trim(), 'Game name')

  if (nameError) {
    setError('game_name', nameError)
  }

  const startTimeError = required(startTime.value, 'Start Time')

  if (startTimeError) {
    setError('start_time', startTimeError)
  }

  if (isThresholdIncremental.value) {
    const setCountError = required(setCount.value, 'Number of sets')

    if (setCountError) {
      setError('set_count', setCountError)
    } else if (Number(setCount.value) < 1) {
      setError('set_count', 'Number of sets must be at least 1.')
    }
  }

  if (!selectedTeamIds.value.length) {
    setError('team_ids', 'Select at least one team for this game.')
  }

  if (hasErrors()) {
    return
  }

  saving.value = true

  try {
    const payload = {
      game_name: gameName.value.trim(),
      start_time: startTime.value,
      end_time: endTime.value || null,
      venue_name: venue.value.trim() || null,
      round: round.value.trim() || null,
      team_ids: selectedTeamIds.value.map(id => Number(id))
    }

    if (isThresholdIncremental.value) {
      payload.set_count = Number(setCount.value)
    }

    await gameStore.editGame(props.game.game_id, payload)
    emit('success')
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="game-form">
    <p class="form-sport-label">
      <strong>Sport:</strong>
      {{ game.sport || '—' }}
      <span class="form-sport-type">
        ({{ game.scoring_type }})
      </span>
    </p>

    <Input
      id="game-name"
      v-model="gameName"
      label="Game name"
      placeholder="Enter game name"
      :error="errors.game_name"
    />

    <div class="form-group">
      <span class="form-label">Teams</span>
      <p class="form-hint">
        Select participating teams for this match.
      </p>

      <div
        v-if="!eventTeams.length"
        class="teams-empty"
      >
        No teams for this event.
      </div>

      <div
        v-else
        class="team-checkbox-list"
        :class="{ 'team-checkbox-list-error': errors.team_ids }"
      >
        <label
          v-for="team in eventTeams"
          :key="team.team_id"
          class="team-checkbox-item"
        >
          <input
            v-model="selectedTeamIds"
            type="checkbox"
            :value="team.team_id"
          >
          <span
            class="team-color-dot"
            :style="{ backgroundColor: team.team_color }"
          />
          <span class="team-checkbox-name">
            {{ team.team_name }}
          </span>
        </label>
      </div>

      <p
        v-if="errors.team_ids"
        class="form-error-text"
      >
        {{ errors.team_ids }}
      </p>
    </div>

    <Input
      id="edit-start-time"
      v-model="startTime"
      type="datetime-local"
      label="Start Time"
      :error="errors.start_time"
    />

    <Input
      id="edit-end-time"
      v-model="endTime"
      type="datetime-local"
      label="End Time"
    />

    <Input
      id="edit-venue"
      v-model="venue"
      label="Venue"
      placeholder="Enter venue"
    />

    <Input
      v-if="isThresholdIncremental"
      id="edit-set-count"
      v-model="setCount"
      type="number"
      min="1"
      label="Number of sets played"
      :error="errors.set_count"
    />

    <Input
      id="edit-round"
      v-model="round"
      label="Round"
      placeholder="e.g. Semi-finals"
    />

    <div class="game-form-actions">
      <button
        type="button"
        class="cancel-btn"
        @click="emit('close')"
      >
        Cancel
      </button>

      <PrimaryButton
        label="Save changes"
        type="button"
        icon="fas fa-check"
        :loading="saving"
        :disabled="saving"
        @click="submitGame"
      />
    </div>
  </div>
</template>

<style scoped>
.game-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 1.25rem;
  border-radius: 12px;
  background: white;
  border: 1px solid var(--border-color);
}

.form-sport-label {
  margin: 0;
  font-size: 0.95rem;
}

.form-sport-type {
  color: var(--text-muted);
  font-weight: 600;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 700;
}

.form-hint {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.form-error-text {
  color: var(--adnu-danger);
  font-size: 12px;
  font-weight: 600;
}

.teams-empty {
  padding: 0.85rem 1rem;
  border-radius: var(--radius-md);
  background: #f9fafb;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.team-checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background: #f9fafb;
  max-height: 220px;
  overflow-y: auto;
}

.team-checkbox-list-error {
  border-color: var(--adnu-danger);
}

.team-checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.45rem 0.5rem;
  border-radius: 8px;
  cursor: pointer;
}

.team-checkbox-item:hover {
  background: white;
}

.team-color-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  flex-shrink: 0;
}

.team-checkbox-name {
  font-size: 0.95rem;
  font-weight: 600;
}

.game-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}

.cancel-btn {
  border: none;
  padding: 12px 18px;
  border-radius: var(--radius-md);
  background: #e5e7eb;
  color: #374151;
  font-weight: 700;
  cursor: pointer;
}
</style>
