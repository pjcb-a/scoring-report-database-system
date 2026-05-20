<script setup>

defineProps({

  modelValue: {
    type: [String, Number],
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

  error: {
    type: String,
    default: ''
  },

  type: {
    type: String,
    default: 'text'
  }
})

const emit = defineEmits([
  'update:modelValue'
])

</script>

<template>

  <div class="input-wrapper">

    <label
      v-if="label"
      class="input-label"
    >
      {{ label }}
    </label>

    <input
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      class="input-field"
      :class="{ error: error }"
      @input="
        emit(
          'update:modelValue',
          $event.target.value
        )
      "
    >

    <p
      v-if="error"
      class="input-error"
    >
      {{ error }}
    </p>

  </div>

</template>

<style scoped>

.input-wrapper {

  display: flex;

  flex-direction: column;

  gap: 8px;
}

.input-label {

  font-size: 14px;

  font-weight: 600;

  color: var(--text-main);
}

.input-field {

  width: 100%;

  padding: 12px 14px;

  border-radius: var(--radius-md);

  border:
    1px solid var(--border-color);

  background-color:
    var(--white);

  color: var(--text-main);

  transition: var(--transition-fast);
}

.input-field:focus {

  outline: none;

  border-color:
    var(--adnu-blue-dark);

  box-shadow:
    0 0 0 3px rgba(
      0,
      56,
      168,
      0.15
    );
}

.input-field.error {

  border-color:
    var(--adnu-danger);
}

.input-error {

  font-size: 13px;

  color: var(--adnu-danger);
}

</style>