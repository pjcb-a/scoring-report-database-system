<script setup>
import { reactive } from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const emit = defineEmits([
  'submit'
])

const form = reactive({

  event_name: '',

  start_day: '',

  end_day: '',

  status: 'Upcoming'
})

const submitForm = () => {
  if (
    !form.event_name.trim() ||
    !form.start_day ||
    !form.end_day ||
    !form.status
  ) {
    return
  }

  emit('submit', {
    ...form
  })

  form.event_name = ''
  form.start_day = ''
  form.end_day = ''

  form.status = 'Upcoming'
}
</script>

<template>

  <form
    class="event-form"
    @submit.prevent="submitForm"
  >

    <Input
      v-model="form.event_name"
      label="Event Name"
      placeholder="Enter event name"
    />

    <Input
      v-model="form.start_day"
      type="date"
      label="Start Date"
    />

    <Input
      v-model="form.end_day"
      type="date"
      label="End Date"
    />

    <div class="input-group">

      <label>
        Status
      </label>

      <select
        v-model="form.status"
        class="base-input"
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

    <div class="form-actions">

      <PrimaryButton>
        Save Event
      </PrimaryButton>

    </div>

  </form>

</template>

<style scoped>
.event-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
