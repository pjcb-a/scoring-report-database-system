<script setup>
import {
  computed,
  reactive
} from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const props = defineProps({

  gameScores: Array,

  criteria: Array,

  judges: Array
})

const emit = defineEmits([
  'success',
  'close'
])

const form = reactive({

  game_score_id: '',

  criteria_id: '',

  judge_id: '',

  score_value: ''
})

const selectedGameScore = computed(() => {
  return props.gameScores.find(
    score => Number(score.game_score_id) === Number(form.game_score_id)
  )
})

const filteredCriteria = computed(() => {
  if (!selectedGameScore.value?.sport) {
    return props.criteria
  }

  return props.criteria.filter(
    criterion => criterion.sport === selectedGameScore.value.sport
  )
})

const submitForm = () => {
  if (
    !form.game_score_id ||
    !form.criteria_id ||
    !form.judge_id ||
    form.score_value === '' ||
    Number(form.score_value) < 0
  ) {
    return
  }

  emit('submit', {
    game_score_id: Number(form.game_score_id),
    criteria_id: Number(form.criteria_id),
    judge_id: Number(form.judge_id),
    score_value: Number(form.score_value)
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
          -
          {{ score.event }}
          -
          {{ score.sport }}
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
          v-for="criterion in filteredCriteria"
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
      min="0"
      placeholder="Enter score"
    />

    <div class="form-actions">

     <button

      type="button"

      class="cancel-btn"

      @click="$emit('close')"
    >
      Cancel
    </button>

    <button

      type="submit"

      class="save-btn"

      :disabled="saving"
    >

      <i
        v-if="saving"
        class="fa-solid fa-spinner fa-spin"
      ></i>

      <i
        v-else
        class="fa-solid fa-check"
      ></i>

      {{ saving ? 'Saving...' : 'Submit Score' }}

    </button>

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
