<script setup>

import { computed, onMounted, ref } from 'vue'

import Input
  from '@/components/ui/Input.vue'

import PrimaryButton
  from '@/components/ui/PrimaryButton.vue'

import {

  required

} from '@/utils/validators'

import {

  createValidation

} from '@/utils/validation'

import {

  useGameStore

} from '../store/gameStore'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  getSportsByEvent

} from '@/features/sports/services/sportService'

import {

  getTeamsByEvent

} from '@/features/teams/services/teamService'


const emit = defineEmits([

  'success',

  'close'
])

const gameStore =
  useGameStore()

const eventContextStore =
  useEventContextStore()

const eventSportId =
  ref('')

const startTime =
  ref('')

const endTime =
  ref('')

const venue =
  ref('')

const setCount =
  ref('')

const round =
  ref('')

const selectedTeamIds =
  ref([])

const saving =
  ref(false)

const eventSports =
  ref([])

const eventTeams =
  ref([])

const selectedEventSport =
  computed(() =>
    eventSports.value.find(
      sport =>
        Number(sport.event_sport_id)
        === Number(eventSportId.value)
    )
  )

const isThresholdIncremental =
  computed(() =>
    selectedEventSport.value?.scoring_type
    === 'Threshold Incremental'
  )

const {

  errors,

  setError,

  clearErrors,

  hasErrors

} = createValidation()

onMounted(async () => {

  if (
    !eventContextStore.currentEventId
  ) {
    return
  }

  const eventId =
    eventContextStore.currentEventId

  try {

    const [sportsResponse, teamsResponse] =
      await Promise.all([

        getSportsByEvent(eventId),

        getTeamsByEvent(eventId)
      ])

    eventSports.value =
      sportsResponse?.data || []

    eventTeams.value =
      teamsResponse?.data || []

  } catch (err) {

    console.error(err)
  }
})

const submitGame =
  async () => {

    if (saving.value) {
      return
    }

    clearErrors()

    const eventSportError =
      required(

        eventSportId.value,

        'Event Sport'
      )

    if (eventSportError) {

      setError(

        'event_sport_id',

        eventSportError
      )
    }

    const startTimeError =
      required(

        startTime.value,

        'Start Time'
      )

    if (startTimeError) {

      setError(

        'start_time',

        startTimeError
      )
    }

    if (isThresholdIncremental.value) {

      const setCountError =
        required(

          setCount.value,

          'Number of sets'
        )

      if (setCountError) {

        setError(

          'set_count',

          setCountError
        )
      } else if (Number(setCount.value) < 1) {

        setError(

          'set_count',

          'Number of sets must be at least 1.'
        )
      }
    }

    if (!selectedTeamIds.value.length) {

      setError(

        'team_ids',

        'Select at least one team for this game.'
      )
    }

    if (hasErrors()) {
      return
    }

    saving.value = true

    try {

      const payload = {

        event_sport_id:
          Number(eventSportId.value),

        start_time:
          startTime.value,

        end_time:
          endTime.value || null,

        venue_name:
          venue.value.trim() || null,

        round:
          round.value.trim() || null,

        team_ids:
          selectedTeamIds.value.map(
            id => Number(id)
          )
      }

      if (isThresholdIncremental.value) {

        payload.set_count =
          Number(setCount.value)
      }

      await gameStore.addGame(payload)

      eventSportId.value = ''

      startTime.value = ''

      endTime.value = ''

      venue.value = ''

      setCount.value = ''

      round.value = ''

      selectedTeamIds.value = []

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

    <div class="form-group">

      <label
        for="event-sport"
        class="form-label"
      >
        Event Sport
      </label>

      <select
        id="event-sport"
        name="event_sport_id"
        v-model="eventSportId"
        class="form-select"
        :class="{
          'form-select-error':
            errors.event_sport_id
        }"
      >

        <option
          disabled
          value=""
        >
          Select event sport
        </option>

        <option
          v-for="sport in eventSports"
          :key="sport.event_sport_id"
          :value="sport.event_sport_id"
        >
          {{ sport.sport_name }}
          ({{ sport.scoring_type }})
        </option>

      </select>

      <p
        v-if="errors.event_sport_id"
        class="form-error-text"
      >
        {{ errors.event_sport_id }}
      </p>

    </div>

    <div class="form-group">

      <span class="form-label">
        Teams
      </span>

      <p class="form-hint">
        Select any number of teams from this event.
      </p>

      <div
        v-if="!eventTeams.length"
        class="teams-empty"
      >
        No teams for this event. Add teams on the Teams tab first.
      </div>

      <div
        v-else
        class="team-checkbox-list"
        :class="{
          'team-checkbox-list-error':
            errors.team_ids
        }"
      >

        <label
          v-for="team in eventTeams"
          :key="team.team_id"
          class="team-checkbox-item"
        >

          <input
            type="checkbox"
            :value="team.team_id"
            v-model="selectedTeamIds"
          />

          <span
            class="team-color-dot"
            :style="{
              backgroundColor:
                team.team_color
            }"
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
      id="start-time"
      name="start_time"
      v-model="startTime"
      type="datetime-local"
      label="Start Time"
      :error="errors.start_time"
    />

    <Input
      id="end-time"
      name="end_time"
      v-model="endTime"
      type="datetime-local"
      label="End Time"
    />

    <Input
      id="venue"
      name="venue"
      v-model="venue"
      label="Venue"
      placeholder="Enter venue"
    />

    <Input
      v-if="isThresholdIncremental"
      id="set-count"
      name="set_count"
      v-model="setCount"
      type="number"
      min="1"
      label="Number of sets played"
      placeholder="e.g. 3"
      :error="errors.set_count"
    />

    <p
      v-if="isThresholdIncremental"
      class="form-hint"
    >
      Set scores are entered later when you finalize the match in Scoring.
    </p>

    <Input
      id="round"
      name="round"
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
        label="Create Game"
        type="button"
        icon="fas fa-plus"
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

  border:
    1px solid var(--border-color);
}

.form-group {

  display: flex;

  flex-direction: column;

  gap: 8px;
}

.form-label {

  font-weight: 700;

  color:
    var(--text-main);
}

.form-hint {

  margin: 0;

  font-size: 0.85rem;

  color: var(--text-muted);
}

.form-select {

  padding: 12px;

  border-radius:
    var(--radius-md);

  border:
    1px solid var(--border-color);

  background-color:
    var(--white);

  transition:
    var(--transition-fast);

  font-size: 14px;
}

.form-select:focus {

  outline: none;

  border-color:
    var(--adnu-blue-light);

  box-shadow:
    0 0 0 3px rgba(59, 130, 246, 0.15);
}

.form-select-error {

  border-color:
    var(--adnu-danger);
}

.form-error-text {

  color:
    var(--adnu-danger);

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

  border:
    1px solid var(--border-color);

  background: #f9fafb;

  max-height: 220px;

  overflow-y: auto;
}

.team-checkbox-list-error {

  border-color:
    var(--adnu-danger);
}

.team-checkbox-item {

  display: flex;

  align-items: center;

  gap: 0.65rem;

  padding: 0.45rem 0.5rem;

  border-radius: 8px;

  cursor: pointer;

  transition: 0.15s ease;
}

.team-checkbox-item:hover {

  background: white;
}

.team-checkbox-item input {

  width: 16px;

  height: 16px;

  cursor: pointer;
}

.team-color-dot {

  width: 18px;

  height: 18px;

  border-radius: 50%;

  border:
    1px solid var(--border-color);

  flex-shrink: 0;
}

.team-checkbox-name {

  font-size: 0.95rem;

  font-weight: 600;

  color: var(--text-main);
}

button {
  border: none;
  outline: none;
  padding: 12px 18px;
  border-radius:
    var(--radius-md);
  cursor: pointer;
  font-weight: 700;
  transition: var(--transition-fast);
  color: var(--white);
  box-shadow: var(--shadow-sm);
  background-color: var(--adnu-danger-strong);
}

button:hover {
  background-color: var(--adnu-danger);
  transition: var(--transition-fast);
}

.game-form-actions {

  display: flex;

  justify-content: flex-end;

  gap: 12px;

  margin-top: 10px;
}

</style>
