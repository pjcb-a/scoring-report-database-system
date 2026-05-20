<script setup>
import { reactive } from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const props = defineProps({

  scoringTypes: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  'submit'
])

const form = reactive({

  sport_name: '',

  scoring_type_id: ''
})

const submitForm = () => {
  if (
    !form.sport_name.trim() ||
    !form.scoring_type_id
  ) {
    return
  }

  emit('submit', {
    sport_name: form.sport_name,
    scoring_type_id: Number(form.scoring_type_id)
  })

  form.sport_name = ''

  form.scoring_type_id = ''
}
</script>

<template>

  <form
    class="sport-form"
    @submit.prevent="submitForm"
  >

    <Input
      v-model="form.sport_name"
      label="Sport Name"
      placeholder="Enter sport name"
    />

    <div class="input-group">

      <label>
        Scoring Type
      </label>

      <select
        v-model="form.scoring_type_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select scoring type
        </option>

        <option
          v-for="type in scoringTypes"
          :key="type.scoring_type_id"
          :value="type.scoring_type_id"
        >
          {{ type.type }}
        </option>

      </select>

    </div>

    <div class="form-actions">

      <PrimaryButton>
        Save Sport
      </PrimaryButton>

    </div>

  </form>

</template>

<style scoped>
.sport-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
