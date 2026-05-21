<script setup>

import { ref } from 'vue'

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

  useEventStore

} from '../store/eventStore'


/*
|--------------------------------------------------------------------------
| EMITS
|--------------------------------------------------------------------------
*/

const emit = defineEmits([

  'success',

  'cancel'
])


/*
|--------------------------------------------------------------------------
| STORE
|--------------------------------------------------------------------------
*/

const eventStore =
  useEventStore()


/*
|--------------------------------------------------------------------------
| FORM STATE
|--------------------------------------------------------------------------
*/

const eventName =
  ref('')

const startDay =
  ref('')

const endDay =
  ref('')

const status =
  ref('Upcoming')

const saving =
  ref(false)


/*
|--------------------------------------------------------------------------
| VALIDATION
|--------------------------------------------------------------------------
*/

const {

  errors,

  setError,

  clearErrors,

  hasErrors

} = createValidation()


/*
|--------------------------------------------------------------------------
| SUBMIT EVENT
|--------------------------------------------------------------------------
*/

const submitEvent =
  async () => {

    /*
    ------------------------------------------------------------------------
    PREVENT DUPLICATE SUBMITS
    ------------------------------------------------------------------------
    */

    if (saving.value) {
      return
    }

    clearErrors()

    /*
    ------------------------------------------------------------------------
    EVENT NAME
    ------------------------------------------------------------------------
    */

    const eventNameError =
      required(

        eventName.value,

        'Event Name'
      )

    if (eventNameError) {

      setError(

        'event_name',

        eventNameError
      )
    }

    /*
    ------------------------------------------------------------------------
    START DAY
    ------------------------------------------------------------------------
    */

    const startDayError =
      required(

        startDay.value,

        'Start Day'
      )

    if (startDayError) {

      setError(

        'start_day',

        startDayError
      )
    }

    /*
    ------------------------------------------------------------------------
    END DAY
    ------------------------------------------------------------------------
    */

    const endDayError =
      required(

        endDay.value,

        'End Day'
      )

    if (endDayError) {

      setError(

        'end_day',

        endDayError
      )
    }

    /*
    ------------------------------------------------------------------------
    STOP IF ERRORS
    ------------------------------------------------------------------------
    */

    if (hasErrors()) {
      return
    }

    saving.value = true

    try {

      await eventStore.createEvent({

        event_name:
          eventName.value,

        start_day:
          startDay.value,

        end_day:
          endDay.value,

        status:
          status.value
      })

      /*
      ----------------------------------------------------------------------
      RESET FORM
      ----------------------------------------------------------------------
      */

      eventName.value = ''

      startDay.value = ''

      endDay.value = ''

      status.value = 'Upcoming'

      emit('success')

    } catch (err) {

      console.error(err)

    } finally {

      saving.value = false
    }
  }

</script>

<template>

  <div class="event-form">

    <!--
    --------------------------------------------------------------------------
    EVENT NAME
    --------------------------------------------------------------------------
    -->

    <Input
      id="event-name"
      name="event_name"
      v-model="eventName"
      label="Event Name"
      placeholder="Enter event name"
      :error="errors.event_name"
    />

    <!--
    --------------------------------------------------------------------------
    START DAY
    --------------------------------------------------------------------------
    -->

    <Input
      id="start-day"
      name="start_day"
      type="date"
      v-model="startDay"
      label="Start Day"
      :error="errors.start_day"
    />

    <!--
    --------------------------------------------------------------------------
    END DAY
    --------------------------------------------------------------------------
    -->

    <Input
      id="end-day"
      name="end_day"
      type="date"
      v-model="endDay"
      label="End Day"
      :error="errors.end_day"
    />

    <!--
    --------------------------------------------------------------------------
    STATUS
    --------------------------------------------------------------------------
    -->

    <div class="form-group">

  <label
    for="event-status"
    class="form-label"
  >

    Event Status

  </label>

  <select

    id="event-status"

    name="status"

    v-model="status"

    class="form-select"
  >

    <option value="Upcoming">
      Upcoming
    </option>

    <option value="Active">
      Active
    </option>

    <option value="Completed">
      Completed
    </option>

  </select>

</div>

    <!--
    --------------------------------------------------------------------------
    ACTIONS
    --------------------------------------------------------------------------
    -->

    <div class="event-form-actions">

      <PrimaryButton

        label="Cancel"

        icon="fas fa-times"

        variant="danger"

        @click="emit('cancel')"
      />

      <PrimaryButton

        label="Add Event"
        type="button"
        icon="fas fa-plus"

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
}


/*
|--------------------------------------------------------------------------
| FORM GROUP
|--------------------------------------------------------------------------
*/

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


/*
|--------------------------------------------------------------------------
| ACTIONS
|--------------------------------------------------------------------------
*/

.event-form-actions {

  display: flex;

  justify-content: flex-end;

  gap: 12px;

  margin-top: 10px;
}

</style>