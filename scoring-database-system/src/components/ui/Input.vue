<script setup>
defineProps({
  label: String,

  modelValue: String,

  placeholder: String,

  type: {
    type: String,
    default: 'text'
  }
})

defineEmits(['update:modelValue'])
</script>

<template>

  <div class="input-group">

    <label
      v-if="label"
      class="input-label"
    >
      {{ label }}
    </label>

    <input
      :type="type"
      :placeholder="placeholder"
      :value="modelValue"
      class="base-input"
      @input="$emit('update:modelValue', $event.target.value)"
    />

  </div>

</template>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
}

.base-input {
  width: 100%;

  padding: 12px 14px;

  border: 1px solid var(--border-color);

  border-radius: var(--radius-md);

  background-color: var(--white);

  transition: var(--transition-fast);
}

.base-input:focus {
  border-color: var(--adnu-blue-dark);
}
</style>