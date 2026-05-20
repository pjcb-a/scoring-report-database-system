<script setup>

defineProps({

  message: {
    type: String,
    required: true
  },

  type: {
    type: String,
    default: 'success'
  }
})

</script>

<template>

  <div
    class="toast"
    :class="type"
  >

    {{ message }}

  </div>

</template>

<style scoped>

.toast {

  min-width: 280px;

  padding: 16px 20px;

  border-radius: 12px;

  color: var(--white);

  font-weight: 600;

  box-shadow:
    0 10px 25px rgba(
      0,
      0,
      0,
      0.15
    );
}

.success {

  background-color: var(--adnu-gold);
}

.error {

  background-color: var(--adnu-danger);
}

.warning {

  background-color: var(--adnu-danger-strong);
}

</style>