<script setup>
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { getSportsByEvent } from '@/features/sports/services/sportService'
import SportCriteriaManager from '@/features/sports/components/SportCriteriaManager.vue'
import EventJudgeManager from './EventJudgeManager.vue'

const COMPONENT_SCORE = 'Component Score'

const eventContextStore = useEventContextStore()
const { currentEventId } = storeToRefs(eventContextStore)

const componentSports = ref([])
const selectedEventSportId = ref('')
const loadingSports = ref(false)

const selectedSport = computed(() =>
  componentSports.value.find(
    sport =>
      Number(sport.event_sport_id)
      === Number(selectedEventSportId.value)
  )
)

const loadComponentSports = async () => {
  if (!currentEventId.value) {
    return
  }

  loadingSports.value = true

  try {
    const response = await getSportsByEvent(currentEventId.value)
    const sports = response.data || []

    componentSports.value = sports.filter(
      sport => sport.scoring_type === COMPONENT_SCORE
    )

    if (
      componentSports.value.length
      && !selectedEventSportId.value
    ) {
      selectedEventSportId.value =
        componentSports.value[0].event_sport_id
    }
  } catch (err) {
    console.error(err)
  } finally {
    loadingSports.value = false
  }
}

loadComponentSports()

defineExpose({ loadComponentSports })
</script>

<template>
  <section class="judging-setup">
    <h2>Component score setup</h2>
    <p class="setup-intro">
      Define criteria per component-score sport and register judges for this event before finalizing matches.
    </p>

    <p
      v-if="loadingSports"
      class="setup-hint"
    >
      Loading sports...
    </p>

    <p
      v-else-if="!componentSports.length"
      class="setup-hint"
    >
      No component-score sports in this event. Add a sport with the Component Score scoring type first.
    </p>

    <template v-else>
      <div class="form-group">
        <label class="form-label">
          Component-score sport
        </label>
        <select
          v-model="selectedEventSportId"
          class="base-input"
        >
          <option
            v-for="sport in componentSports"
            :key="sport.event_sport_id"
            :value="sport.event_sport_id"
          >
            {{ sport.sport_name }}
          </option>
        </select>
      </div>

      <SportCriteriaManager
        v-if="selectedEventSportId"
        :key="selectedEventSportId"
        :event-sport-id="Number(selectedEventSportId)"
      />
    </template>

    <EventJudgeManager />
  </section>
</template>

<style scoped>
.judging-setup {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 20px;
  border-radius: 14px;
  background: white;
  border: 1px solid var(--border-color, #e2e8f0);
}

.judging-setup h2 {
  margin: 0;
  font-size: 1.1rem;
}

.setup-intro,
.setup-hint {
  margin: 0;
  color: var(--text-muted, #64748b);
  font-size: 0.9rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 700;
}

.base-input {
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}
</style>
