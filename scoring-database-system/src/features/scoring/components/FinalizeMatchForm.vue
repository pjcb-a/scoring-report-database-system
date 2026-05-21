<script setup>

import {
  computed,
  reactive,
  ref
} from 'vue'

import {
  useScoringStore
} from '../store/scoringStore'

const props = defineProps({

  game: {
    type: Object,
    required: true
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

  game_status:

    props.game?.game_status ||

    'Finished'
})

const statusOptions = [

  'Finished',

  'Default Win',

  'Forfeit',

  'Suspended',

  'Cancelled'
]

const gameTitle =
  computed(() => {

    const teams =

      props.game?.teams || []

    if (teams.length >= 2) {

      return `${teams[0]} vs ${teams[1]}`
    }

    return 'Game Match'
  })

const submitForm =
  async () => {

    if (!form.game_status) {
      return
    }

    saving.value = true

    try {

      await scoringStore.finalizeGame(

        props.game.game_id,

        {
          game_status:
            form.game_status
        }
      )

      emit('success')

      emit('close')

    } catch (err) {

      console.error(err)

    } finally {

      saving.value = false
    }
  }

</script>

<template>

  <form
    class="finalize-form"
    @submit.prevent="submitForm"
  >

    <div class="form-header">

      <h2>
        Finalize Match
      </h2>

      <p>
        {{ gameTitle }}
      </p>

    </div>

    <div class="form-group">

      <label>
        Match Status
      </label>

      <select v-model="form.game_status">

        <option
          v-for="status in statusOptions"
          :key="status"
          :value="status"
        >
          {{ status }}
        </option>

      </select>

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

        {{ saving
          ? 'Finalizing...'
          : 'Finalize Match'
        }}

      </button>

    </div>

  </form>

</template>

<style scoped>
.finalize-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.match-summary h3 {
  margin: 0;
  font-size: 1.15rem;
}

.match-summary p {
  margin: 0.35rem 0 0;
  color: var(--text-muted);
}

.match-meta {
  font-size: 0.9rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 700;
}

.team-score-block {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.team-score-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.team-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.set-scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
}

.winner-option {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-btn {
  padding: 12px 18px;
  border: none;
  border-radius: var(--radius-md, 8px);
  background: #e5e7eb;
  color: #374151;
  font-weight: 700;
  cursor: pointer;
}
</style>
