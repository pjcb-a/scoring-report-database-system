<script setup>

import {
  reactive,
  computed,
  ref
} from 'vue'

import {
  useScoringStore
} from '../store/scoringStore'

const props = defineProps({

  gameScores: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'success',
  'close'
])

const scoringStore =
  useScoringStore()

const saving = ref(false)

const form = reactive({

  game_score_id: '',

  score_value: ''
})

const selectedGameScore =
  computed(() => {

    return props.gameScores.find(

      score =>

        Number(score.game_score_id)

        ===

        Number(form.game_score_id)
    )
  })

const submitForm =
  async () => {

    if (
      !form.game_score_id ||
      form.score_value === ''
    ) {
      return
    }

    saving.value = true

    try {

      await scoringStore.createScore({

        game_score_id:
          Number(form.game_score_id),

        score_value:
          Number(form.score_value)
      })

      emit('success')

      emit('close')

      form.game_score_id = ''
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
  class="score-form"
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
        class="fa-solid fa-floppy-disk"
      ></i>

      {{ saving ? 'Saving...' : 'Save Score' }}

    </button>

  </div>

</form>

</template>

<style scoped>
.score-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
