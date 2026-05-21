<script setup>

import { onMounted, ref } from 'vue'

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

  useSportStore

} from '../store/sportStore'

import {

  getScoringTypes

} from '../services/sportService'


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

const sportStore =
  useSportStore()


/*
|--------------------------------------------------------------------------
| FORM STATE
|--------------------------------------------------------------------------
*/

const sportName =
  ref('')

const scoringTypeId =
  ref('')

const saving =
  ref(false)

const scoringTypes =
  ref([])


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
| LOAD SCORING TYPES
|--------------------------------------------------------------------------
*/

onMounted(async () => {

  try {

    const response = await getScoringTypes()
    scoringTypes.value = response?.data || []

  } catch (err) {

    console.error(err)
  }
})


/*
|--------------------------------------------------------------------------
| SUBMIT SPORT
|--------------------------------------------------------------------------
*/

const submitSport =
  async () => {

    /*
    ------------------------------------------------------------------------
    PREVENT DUPLICATE SUBMITS
    ------------------------------------------------------------------------
    */

    if (saving.value) {
      return
    }

    clearErrors()

    /*
    ------------------------------------------------------------------------
    SPORT NAME
    ------------------------------------------------------------------------
    */

    const sportNameError =
      required(

        sportName.value,

        'Sport Name'
      )

    if (sportNameError) {

      setError(

        'sport_name',

        sportNameError
      )
    }

    /*
    ------------------------------------------------------------------------
    SCORING TYPE
    ------------------------------------------------------------------------
    */

    const scoringTypeError =
      required(

        scoringTypeId.value,

        'Scoring Type'
      )

    if (scoringTypeError) {

      setError(

        'scoring_type_id',

        scoringTypeError
      )
    }

    /*
    ------------------------------------------------------------------------
    STOP IF ERRORS
    ------------------------------------------------------------------------
    */

    if (hasErrors()) {
      return
    }

    saving.value = true

    try {

      await sportStore.addSport({

        sport_name:
          sportName.value,

        scoring_type_id:
          Number(scoringTypeId.value)
      })

      /*
      ----------------------------------------------------------------------
      RESET FORM
      ----------------------------------------------------------------------
      */

      sportName.value = ''

      scoringTypeId.value = ''

      emit('success')

    } catch (err) {

      console.error(err)

    } finally {

      saving.value = false
    }
  }

</script>

<template>

  <div class="sport-form">

    <!--
    --------------------------------------------------------------------------
    SPORT NAME
    --------------------------------------------------------------------------
    -->

    <Input
      id="sport-name"
      name="sport_name"
      v-model="sportName"
      label="Sport Name"
      placeholder="Enter sport name"
      :error="errors.sport_name"
    />

    <!--
    --------------------------------------------------------------------------
    SCORING TYPE
    --------------------------------------------------------------------------
    -->

    <div class="form-group">

      <label
        for="scoring-type"
        class="form-label"
      >

        Scoring Type

      </label>

      <select

        id="scoring-type"

        name="scoring_type_id"

        v-model="scoringTypeId"

        class="form-select"

        :class="{
          'form-select-error':
            errors.scoring_type_id
        }"
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

      <p
        v-if="errors.scoring_type_id"
        class="form-error-text"
      >
        {{ errors.scoring_type_id }}
      </p>

    </div>

    <!--
    --------------------------------------------------------------------------
    ACTIONS
    --------------------------------------------------------------------------
    -->

    <div class="sport-form-actions">

      <button
        type="button"

        class="cancel-btn"

        @click="emit('close')"
      >
        Cancel
      </button>

      <PrimaryButton

        label="Add Sport"
        type="button"
        icon="fas fa-plus"

        :loading="saving"

        :disabled="saving"

        @click="submitSport"
      />

    </div>

  </div>

</template>

<style scoped>

.sport-form {

  display: flex;

  flex-direction: column;

  gap: 20px;
}


/*
|--------------------------------------------------------------------------
| FORM GROUP
|--------------------------------------------------------------------------
*/

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

.form-select {

  padding: 12px;

  border-radius:
    var(--radius-md);

  border:
    1px solid var(--border-color);

  background-color:
    var(--white);

  transition:
    var(--transition-fast);

  font-size: 14px;
}

.form-select:focus {

  outline: none;

  border-color:
    var(--adnu-blue-light);

  box-shadow:
    0 0 0 3px rgba(59, 130, 246, 0.15);
}

.form-select-error {

  border-color:
    var(--adnu-danger);
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

/*
|--------------------------------------------------------------------------
| ACTIONS
|--------------------------------------------------------------------------
*/

.sport-form-actions {

  display: flex;

  justify-content: flex-end;

  gap: 12px;

  margin-top: 10px;
}

</style>
