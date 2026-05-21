<script setup>

import { ref } from 'vue'

import Input
  from '@/components/ui/Input.vue'

import PrimaryButton
  from '@/components/ui/PrimaryButton.vue'

import {

  required

} from '@/utils/validators'

import {

  createValidation

} from '@/utils/validation'

import {

  useTeamStore

} from '../store/teamStore'


/*
|--------------------------------------------------------------------------
| EMITS
|--------------------------------------------------------------------------
*/

const emit = defineEmits([

  'success',

  'close'
])


/*
|--------------------------------------------------------------------------
| STORE
|--------------------------------------------------------------------------
*/

const teamStore =
  useTeamStore()


/*
|--------------------------------------------------------------------------
| FORM STATE
|--------------------------------------------------------------------------
*/

const teamName =
  ref('')

const teamColor =
  ref('#2563eb')

const saving =
  ref(false)


/*
|--------------------------------------------------------------------------
| VALIDATION
|--------------------------------------------------------------------------
*/

const {

  errors,

  setError,

  clearErrors,

  hasErrors

} = createValidation()


/*
|--------------------------------------------------------------------------
| SUBMIT TEAM
|--------------------------------------------------------------------------
*/

const submitTeam =
  async () => {

    if (saving.value) {
      return
    }

    clearErrors()

    const teamNameError =
      required(

        teamName.value,

        'Team Name'
      )

    if (teamNameError) {

      setError(

        'team_name',

        teamNameError
      )
    }

    const teamColorError =
      required(

        teamColor.value,

        'Team Color'
      )

    if (teamColorError) {

      setError(

        'team_color',

        teamColorError
      )
    }

    if (hasErrors()) {
      return
    }

    saving.value = true

    try {

      await teamStore.addTeam({

        team_name:
          teamName.value.trim(),

        team_color:
          teamColor.value
      })

      teamName.value = ''

      teamColor.value = '#2563eb'

      emit('success')

    } catch (err) {

      console.error(err)

    } finally {

      saving.value = false
    }
  }

</script>

<template>

  <div class="team-form">

    <Input
      id="team-name"
      name="team_name"
      v-model="teamName"
      label="Team Name"
      placeholder="Enter team name"
      :error="errors.team_name"
    />

    <div class="form-group">

      <label
        for="team-color"
        class="form-label"
      >
        Team Color
      </label>

      <div class="color-input-row">

        <input
          id="team-color"
          name="team_color"
          v-model="teamColor"
          type="color"
          class="color-picker"
          :class="{
            'color-picker-error':
              errors.team_color
          }"
        />

        <Input
          id="team-color-hex"
          name="team_color_hex"
          v-model="teamColor"
          placeholder="#2563eb"
        />

      </div>

      <p
        v-if="errors.team_color"
        class="form-error-text"
      >
        {{ errors.team_color }}
      </p>

    </div>

    <div class="team-form-actions">

      <button
        type="button"
        class="cancel-btn"
        @click="emit('close')"
      >
        Cancel
      </button>

      <PrimaryButton
        label="Add Team"
        type="button"
        icon="fas fa-plus"
        :loading="saving"
        :disabled="saving"
        @click="submitTeam"
      />

    </div>

  </div>

</template>

<style scoped>

.team-form {

  display: flex;

  flex-direction: column;

  gap: 20px;

  padding: 1.25rem;

  border-radius: 12px;

  background: white;

  border:
    1px solid var(--border-color);
}

.form-group {

  display: flex;

  flex-direction: column;

  gap: 8px;
}

.form-label {

  font-weight: 700;

  color:
    var(--text-main);
}

.color-input-row {

  display: flex;

  align-items: flex-start;

  gap: 12px;
}

.color-picker {

  width: 52px;

  height: 44px;

  padding: 4px;

  border-radius:
    var(--radius-md);

  border:
    1px solid var(--border-color);

  background-color:
    var(--white);

  cursor: pointer;
}

.color-picker-error {

  border-color:
    var(--adnu-danger);
}

.color-input-row :deep(.input-group) {

  flex: 1;
}

.form-error-text {

  color:
    var(--adnu-danger);

  font-size: 12px;

  font-weight: 600;
}

button {
  border: none;
  outline: none;
  padding: 12px 18px;
  border-radius:
    var(--radius-md);
  cursor: pointer;
  font-weight: 700;
  transition: var(--transition-fast);
  color: var(--white);
  box-shadow: var(--shadow-sm);
  background-color: var(--adnu-danger-strong);
}

button:hover {
  background-color: var(--adnu-danger);
  transition: var(--transition-fast);
}

.team-form-actions {

  display: flex;

  justify-content: flex-end;

  gap: 12px;

  margin-top: 10px;
}

</style>
