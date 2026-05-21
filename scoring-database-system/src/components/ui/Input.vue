<script setup>

import {

  computed

} from 'vue'


const props = defineProps({

  modelValue: {
    type: [

      String,

      Number
    ],

    default: ''
  },

  label: {
    type: String,
    default: ''
  },

  placeholder: {
    type: String,
    default: ''
  },

  type: {
    type: String,
    default: 'text'
  },

  error: {
    type: String,
    default: ''
  },

  disabled: {
    type: Boolean,
    default: false
  },

  id: {
    type: String,
    default: ''
  },

  name: {
    type: String,
    default: ''
  },

  min: {
    type: [String, Number],
    default: undefined
  },

  max: {
    type: [String, Number],
    default: undefined
  },

  step: {
    type: [String, Number],
    default: undefined
  }
})


const emit = defineEmits([
  'update:modelValue'
])


/*
|--------------------------------------------------------------------------
| GENERATED INPUT ID
|--------------------------------------------------------------------------
|
| Prevent duplicate ids while supporting accessibility.
|
*/

const inputId =
  computed(() => {

    return (

      props.id

      ||

      props.name

      ||

      `input-${Math.random()
        .toString(36)
        .slice(2, 9)}`
    )
  })

</script>

<template>

  <div class="input-group">

    <!--
    --------------------------------------------------------------------------
    LABEL
    --------------------------------------------------------------------------
    -->

    <label

      v-if="label"

      :for="inputId"

      class="input-label"
    >

      {{ label }}

    </label>

    <!--
    --------------------------------------------------------------------------
    INPUT
    --------------------------------------------------------------------------
    -->

    <input

      :id="inputId"

      :name="name || inputId"

      :type="type"

      :value="modelValue"

      :placeholder="placeholder"

      :disabled="disabled"

      :min="min"

      :max="max"

      :step="step"

      class="input-field"

      :class="{

        'input-error': error
      }"

      @input="

        emit(
          'update:modelValue',
          $event.target.value
        )

      "
    />

    <!--
    --------------------------------------------------------------------------
    ERROR
    --------------------------------------------------------------------------
    -->

    <p
      v-if="error"
      class="input-error-text"
    >

      {{ error }}

    </p>

  </div>

</template>

<style scoped>

.input-group {

  display: flex;

  flex-direction: column;

  gap: 8px;
}


/*
|--------------------------------------------------------------------------
| LABEL
|--------------------------------------------------------------------------
*/

.input-label {

  font-weight: 700;

  color:
    var(--text-main);
}


/*
|--------------------------------------------------------------------------
| INPUT
|--------------------------------------------------------------------------
*/

.input-field {

  padding: 12px;

  border-radius:
    var(--radius-md);

  border:
    1px solid var(--border-color);

  transition:
    var(--transition-fast);

  font-size: 14px;

  background-color:
    var(--white);
}

.input-field:focus {

  outline: none;

  border-color:
    var(--adnu-blue-light);

  box-shadow:
    0 0 0 3px rgba(59, 130, 246, 0.15);
}


/*
|--------------------------------------------------------------------------
| ERROR
|--------------------------------------------------------------------------
*/

.input-error {

  border-color:
    var(--adnu-danger);
}

.input-error-text {

  color:
    var(--adnu-danger);

  font-size: 12px;

  font-weight: 600;
}

</style>