<script setup>
defineProps({
  disabled: {
    type: Boolean,
    default: false
  }
})
</script>

<template>

  <button
    class="btn-primary"
    :disabled="disabled"
  >
    <slot />
  </button>

</template>

<style scoped>
.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>