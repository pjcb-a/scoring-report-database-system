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

  game_date: '',

  status: 'Scheduled'
})

const submitForm = () => {

  emit('submit', {
    ...form
  })

  form.event_sport_id = ''

  form.round = ''

  form.game_date = ''

  form.status = 'Scheduled'
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
          {{ eventSport.event }}
          -
          {{ eventSport.sport }}
        </option>

      </select>

    </div>

    <Input
      v-model="form.round"
      label="Round"
      placeholder="e.g. Finals"
    />

    <Input
      v-model="form.game_date"
      type="datetime-local"
      label="Game Date"
    />

    <div class="input-group">

      <label>
        Status
      </label>

      <select
        v-model="form.status"
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