<script setup>

const props = defineProps({

  label: {
    type: String,
    default: 'Submit'
  },

  variant: {
    type: String,
    default: 'primary'
  },

  loading: {
    type: Boolean,
    default: false
  },

  disabled: {
    type: Boolean,
    default: false
  },

  type: {
    type: String,
    default: 'button'
  }
})

</script>

<template>

  <button
    :type="type"
    class="primary-button"
    :class="variant"
    :disabled="disabled || loading"
  >

    <span v-if="loading">
      Loading...
    </span>

    <span v-else>
      {{ label }}
    </span>

  </button>

</template>

<style scoped>

.primary-button {

  border: none;

  outline: none;

  padding: 12px 18px;

  border-radius: var(--radius-md);

  cursor: pointer;

  font-weight: 700;

  transition: var(--transition-fast);

  color: var(--white);

  box-shadow: var(--shadow-sm);
}

.primary-button:hover {

  transform: translateY(-1px);

  box-shadow: var(--shadow-md);
}

.primary-button:disabled {

  opacity: 0.6;

  cursor: not-allowed;
}

.primary {

  background-color:
    var(--adnu-blue-dark);
}

.primary:hover {

  background-color:
    var(--adnu-blue-navy);
}

.danger {

  background-color:
    var(--adnu-danger);
}

.danger:hover {

  background-color:
    var(--adnu-danger-strong);
}

.gold {

  background-color:
    var(--adnu-gold);

  color: var(--text-main);
}

</style>