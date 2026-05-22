<script setup>
import { computed, ref, watch } from 'vue'
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import { required } from '@/utils/validators'
import { createValidation } from '@/utils/validation'
import { useEventStore } from '../store/eventStore'
import {
  EVENT_STATUS_OPTIONS,
  normalizeEventStatus
} from '../utils/eventStatus'

const props = defineProps({
  event: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['success', 'close'])

const eventStore = useEventStore()

const isEditMode = computed(() => !!props.event?.event_id)

const eventName = ref('')
const startDay = ref('')
const endDay = ref('')
const status = ref('Upcoming')
const saving = ref(false)

const { errors, setError, clearErrors, hasErrors } = createValidation()

const populateForm = () => {
  if (isEditMode.value) {
    eventName.value = props.event.event_name || ''
    startDay.value = props.event.start_day || ''
    endDay.value = props.event.end_day || ''
    status.value = normalizeEventStatus(props.event.status)
    return
  }

  eventName.value = ''
  startDay.value = ''
  endDay.value = ''
  status.value = 'Upcoming'
}

watch(
  () => props.event?.event_id,
  () => populateForm(),
  { immediate: true }
)

const submitEvent = async () => {
  if (saving.value) {
    return
  }

  clearErrors()

  const eventNameError = required(eventName.value, 'Event Name')

  if (eventNameError) {
    setError('event_name', eventNameError)
  }

  const startDayError = required(startDay.value, 'Start Day')

  if (startDayError) {
    setError('start_day', startDayError)
  }

  const endDayError = required(endDay.value, 'End Day')

  if (endDayError) {
    setError('end_day', endDayError)
  }

  if (
    startDay.value
    && endDay.value
    && endDay.value < startDay.value
  ) {
    setError('end_day', 'End day cannot be before start day.')
  }

  if (hasErrors()) {
    return
  }

  saving.value = true

  const payload = {
    event_name: eventName.value.trim(),
    start_day: startDay.value,
    end_day: endDay.value,
    status: status.value
  }

  try {
    let savedEvent

    if (isEditMode.value) {
      savedEvent = await eventStore.editEvent(
        props.event.event_id,
        payload
      )
    } else {
      savedEvent = await eventStore.createEvent(payload)
      populateForm()
    }

    emit('success', savedEvent)
  } catch (err) {
    console.error(err)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="event-form">
    <h2 class="event-form__title">
      {{ isEditMode ? 'Edit Event' : 'Add Event' }}
    </h2>

    <p
      v-if="isEditMode"
      class="event-form__hint"
    >
      Status is metadata only and does not change scoring or reports behavior.
    </p>

    <Input
      id="event-name"
      v-model="eventName"
      label="Event Name"
      placeholder="Enter event name"
      :error="errors.event_name"
    />

    <Input
      id="start-day"
      v-model="startDay"
      type="date"
      label="Start Day"
      :error="errors.start_day"
    />

    <Input
      id="end-day"
      v-model="endDay"
      type="date"
      label="End Day"
      :error="errors.end_day"
    />

    <div class="form-group">
      <label
        for="event-status"
        class="form-label"
      >
        Event Status
      </label>
      <select
        id="event-status"
        v-model="status"
        class="form-select"
      >
        <option
          v-for="option in EVENT_STATUS_OPTIONS"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
    </div>

    <div class="event-form-actions">
      <button
        type="button"
        class="cancel-btn"
        @click="emit('close')"
      >
        Cancel
      </button>

      <PrimaryButton
        :label="isEditMode ? 'Save Changes' : 'Add Event'"
        type="button"
        :icon="isEditMode ? 'fas fa-check' : 'fas fa-plus'"
        :loading="saving"
        :disabled="saving"
        @click="submitEvent"
      />
    </div>
  </div>
</template>

<style scoped>
.event-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 1.25rem;
  border-radius: 12px;
  background: white;
  border: 1px solid var(--border-color);
}

.event-form__title {
  margin: 0;
  font-size: 1.15rem;
}

.event-form__hint {
  margin: -8px 0 0;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 700;
  color: var(--text-main);
}

.form-select {
  padding: 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  background-color: var(--white);
  font-size: 14px;
}

.form-select:focus {
  outline: none;
  border-color: var(--adnu-blue-light);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
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

.event-form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 10px;
}
</style>
