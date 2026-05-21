<script setup>
import {
  computed,
  reactive
} from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const props = defineProps({

  games: {
    type: Array,
    required: true
  },

  teams: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  'success',
  'close'
])

const form = reactive({

  game_id: '',

  team_id: '',

  score_value: '',

  rank_position: '',

  isWinner: false
})

const selectedGame = computed(() => {
  return props.games.find(
    game => Number(game.game_id) === Number(form.game_id)
  )
})

const scoringType = computed(() => {
  return selectedGame.value?.scoring_type || ''
})

const showRank = computed(() => {
  return [
    'Ranked Timed',
    'Threshold Incremental'
  ].includes(scoringType.value)
})

const showWinner = computed(() => {
  return scoringType.value !== 'Component Score'
})

const submitForm = () => {
  if (
    !form.game_id ||
    !form.team_id ||
    form.score_value === ''
  ) {
    return
  }

  if (
    showRank.value &&
    form.rank_position !== '' &&
    Number(form.rank_position) <= 0
  ) {
    return
  }

  if (Number(form.score_value) < 0) {
    return
  }

  emit('submit', {
    game_id: Number(form.game_id),
    team_id: Number(form.team_id),
    score_value: Number(form.score_value),
    rank_position:
      showRank.value && form.rank_position !== ''
        ? Number(form.rank_position)
        : null,
    isWinner:
      showWinner.value
        ? form.isWinner
        : false
  })

  form.game_id = ''

  form.team_id = ''

  form.score_value = ''

  form.rank_position = ''

  form.isWinner = false
}
</script>

<template>

  <form
    class="score-form"
    @submit.prevent="submitForm"
  >

    <div class="input-group">

      <label>
        Game
      </label>

      <select
        v-model="form.game_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select game
        </option>

        <option
          v-for="game in games"
          :key="game.game_id"
          :value="game.game_id"
        >
          {{ game.event }}
          -
          {{ game.sport }}
          -
          {{ game.round }}
        </option>

      </select>

    </div>

    <div class="input-group">

      <label>
        Team
      </label>

      <select
        v-model="form.team_id"
        class="base-input"
      >

        <option
          disabled
          value=""
        >
          Select team
        </option>

        <option
          v-for="team in teams"
          :key="team.team_id"
          :value="team.team_id"
        >
          {{ team.team_name }}
        </option>

      </select>

    </div>

    <Input
      v-model="form.score_value"
      label="Score Value"
      type="number"
      min="0"
      placeholder="Enter score"
    />

    <Input
      v-if="showRank"
      v-model="form.rank_position"
      label="Rank Position"
      type="number"
      min="1"
      placeholder="Enter rank"
    />

    <div
      v-if="showWinner"
      class="checkbox-group"
    >

      <input
        id="winner"
        v-model="form.isWinner"
        type="checkbox"
      >

      <label for="winner">
        Winner
      </label>

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
