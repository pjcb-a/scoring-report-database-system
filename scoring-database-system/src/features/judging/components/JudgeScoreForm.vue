<script setup>

import {
  reactive,
  ref
} from 'vue'

import {
  useJudgingStore
} from '../stores/judgingStore'

const props = defineProps({

  gameScores: {
    type: Array,
    default: () => []
  },

  criteria: {
    type: Array,
    default: () => []
  },

  judges: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'success',
  'close'
])

const judgingStore =
  useJudgingStore()

const saving = ref(false)

const form = reactive({

  game_score_id: '',

  criteria_id: '',

  judge_id: '',

  score_value: ''
})

const submitForm =
  async () => {

    if (
      !form.game_score_id ||
      !form.criteria_id ||
      !form.judge_id ||
      form.score_value === ''
    ) {
      return
    }

    saving.value = true

    try {

      await judgingStore.createJudgeScore({

        game_score_id:
          Number(form.game_score_id),

        criteria_id:
          Number(form.criteria_id),

        judge_id:
          Number(form.judge_id),

        score_value:
          Number(form.score_value)
      })

      emit('success')

      emit('close')

      form.game_score_id = ''
      form.criteria_id = ''
      form.judge_id = ''
      form.score_value = ''

    } catch (err) {

      console.error(err)

    } finally {

      saving.value = false
    }
  }

</script>

<template>

  <form
  class="judge-form"
  @submit.prevent="submitForm"
>

  <div class="form-group">

    <label>
      Game Score
    </label>

    <select v-model="form.game_score_id">

      <option value="">
        Select Game
      </option>

      <option

        v-for="score in gameScores"

        :key="score.game_score_id"

        :value="score.game_score_id"
      >
        {{ score.team_name }}
      </option>

    </select>

  </div>

  <div class="form-group">

    <label>
      Criteria
    </label>

    <select v-model="form.criteria_id">

      <option value="">
        Select Criteria
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

  <div class="form-group">

    <label>
      Judge
    </label>

    <select v-model="form.judge_id">

      <option value="">
        Select Judge
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

  <div class="form-group">

    <label>
      Score
    </label>

    <input

      v-model="form.score_value"

      type="number"

      min="0"
    />

  </div>

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
