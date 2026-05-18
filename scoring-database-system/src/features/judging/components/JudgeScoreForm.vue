<script setup>
import { reactive } from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const props = defineProps({

  gameScores: Array,

  criteria: Array,

  judges: Array
})

const emit = defineEmits([
  'submit'
])

const form = reactive({

  game_score_id: '',

  criteria_id: '',

  judge_id: '',

  score_value: ''
})

const submitForm = () => {

  emit('submit', {
    ...form
  })

  form.game_score_id = ''

  form.criteria_id = ''

  form.judge_id = ''

  form.score_value = ''
}
</script>

<template>

  <form
    class="judge-form"
    @submit.prevent="submitForm"
  >

    <div class="input-group">

      <label>
        Game Score
      </label>

      <select
        v-model="form.game_score_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select score
        </option>

        <option
          v-for="score in gameScores"
          :key="score.game_score_id"
          :value="score.game_score_id"
        >
          {{ score.team }}
        </option>

      </select>

    </div>

    <div class="input-group">

      <label>
        Criteria
      </label>

      <select
        v-model="form.criteria_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select criteria
        </option>

        <option
          v-for="criterion in criteria"
          :key="criterion.criteria_id"
          :value="criterion.criteria_id"
        >
          {{ criterion.criteria_name }}
        </option>

      </select>

    </div>

    <div class="input-group">

      <label>
        Judge
      </label>

      <select
        v-model="form.judge_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select judge
        </option>

        <option
          v-for="judge in judges"
          :key="judge.judge_id"
          :value="judge.judge_id"
        >
          {{ judge.judge_name }}
        </option>

      </select>

    </div>

    <Input
      v-model="form.score_value"
      label="Judge Score"
      type="number"
      placeholder="Enter score"
    />

    <div class="form-actions">

      <PrimaryButton>
        Save Judge Score
      </PrimaryButton>

    </div>

  </form>

</template>

<style scoped>
.judge-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>