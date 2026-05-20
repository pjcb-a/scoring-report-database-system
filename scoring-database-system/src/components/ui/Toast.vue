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

  <transition name="toast">

    <div
      class="toast"
      :class="type"
    >

      {{ message }}

    </div>

  </transition>

</template>

<style scoped>

.toast {

  min-width: 280px;

  padding: 16px 20px;

  border-radius:
    var(--radius-lg);

  color: var(--white);

  font-weight: 700;

  box-shadow:
    var(--shadow-md);

  transition:
    var(--transition-fast);
}

.success {

  background-color:
    var(--adnu-blue-dark);
}

.error {

  background-color:
    var(--adnu-danger);
}

.warning {

  background-color:
    var(--adnu-danger-strong);
}

.toast-enter-active,
.toast-leave-active {

  transition:
    all 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {

  opacity: 0;

  transform:
    translateY(-10px);
}

</style>