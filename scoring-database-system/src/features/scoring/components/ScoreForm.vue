<script setup>
import { reactive } from 'vue'

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
  'submit'
])

const form = reactive({

  game_id: '',

  team_id: '',

  score_value: '',

  rank_position: '',

  isWinner: false
})

const submitForm = () => {

  emit('submit', {
    ...form
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
      placeholder="Enter score"
    />

    <Input
      v-model="form.rank_position"
      label="Rank Position"
      type="number"
      placeholder="Enter rank"
    />

    <div class="checkbox-group">

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

      <PrimaryButton>
        Save Score
      </PrimaryButton>

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