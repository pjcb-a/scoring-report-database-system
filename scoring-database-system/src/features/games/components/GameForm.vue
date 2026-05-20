<script setup>
import { reactive } from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const props = defineProps({

  eventSports: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  'submit'
])

const form = reactive({

  event_sport_id: '',

  round: '',

  venue_name: '',

  start_date: '',

  end_date: '',

  game_status: 'Scheduled'
})

const submitForm = () => {
  if (
    !form.event_sport_id ||
    !form.start_date ||
    !form.game_status
  ) {
    return
  }

  emit('submit', {
    event_sport_id: Number(form.event_sport_id),
    round: form.round,
    venue_name: form.venue_name,
    start_date: form.start_date,
    end_date: form.end_date || null,
    game_status: form.game_status
  })

  form.event_sport_id = ''

  form.round = ''

  form.venue_name = ''

  form.start_date = ''

  form.end_date = ''

  form.game_status = 'Scheduled'
}
</script>


<template>

  <form
    class="game-form"
    @submit.prevent="submitForm"
  >

    <div class="input-group">

      <label>
        Event Sport
      </label>

      <select
        v-model="form.event_sport_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select event sport
        </option>

        <option
          v-for="eventSport in eventSports"
          :key="eventSport.event_sport_id"
          :value="eventSport.event_sport_id"
        >
          {{ eventSport.event || eventSport.event_name }}
          -
          {{ eventSport.sport || eventSport.sport_name }}
        </option>

      </select>

    </div>

    <Input
      v-model="form.round"
      label="Round"
      placeholder="e.g. Finals"
    />

    <Input
      v-model="form.venue_name"
      label="Venue"
      placeholder="Enter game venue"
    />

    <Input
      v-model="form.start_date"
      type="datetime-local"
      label="Start Date"
    />

    <Input
      v-model="form.end_date"
      type="datetime-local"
      label="End Date"
    />

    <div class="input-group">

      <label>
        Status
      </label>

      <select
        v-model="form.game_status"
        class="base-input"
      >

        <option value="Scheduled">
          Scheduled
        </option>

        <option value="Ongoing">
          Ongoing
        </option>

        <option value="Completed">
          Completed
        </option>

      </select>

    </div>

    <div class="form-actions">

      <PrimaryButton>
        Save Game
      </PrimaryButton>

    </div>

  </form>

</template>

<style scoped>
.game-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
