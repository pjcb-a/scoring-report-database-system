<script setup>

defineProps({

  title: {
    type: String,
    default: 'Confirm Action'
  },

  message: {
    type: String,
    default: 'Are you sure?'
  }
})

const emit = defineEmits([
  'confirm',
  'cancel'
])

</script>

<template>

  <div class="dialog-overlay">

    <div class="dialog-card">

      <h2 class="dialog-title">

        {{ title }}

      </h2>

      <p class="dialog-message">

        {{ message }}

      </p>

      <div class="dialog-actions">

        <button
          class="cancel-button"
          @click="emit('cancel')"
        >
          Cancel
        </button>

        <button
          class="confirm-button"
          @click="emit('confirm')"
        >
          Confirm
        </button>

      </div>

    </div>

  </div>

</template>

<style scoped>

.dialog-overlay {

  position: fixed;

  inset: 0;

  background-color:
    rgba(0, 0, 0, 0.45);

  display: flex;

  align-items: center;

  justify-content: center;

  z-index: 9999;
}

.dialog-card {

  width: 420px;

  background-color:
    var(--white);

  border-radius:
    var(--radius-lg);

  padding: 28px;

  box-shadow:
    var(--shadow-md);
}

.dialog-title {

  font-size: 24px;

  font-weight: 800;

  color:
    var(--text-main);

  margin-bottom: 14px;
}

.dialog-message {

  color:
    var(--text-muted);

  line-height: 1.6;
}

.dialog-actions {

  margin-top: 24px;

  display: flex;

  justify-content: flex-end;

  gap: 12px;
}

.cancel-button,
.confirm-button {

  border: none;

  padding: 10px 18px;

  border-radius:
    var(--radius-md);

  cursor: pointer;

  font-weight: 700;

  transition:
    var(--transition-fast);
}

.cancel-button {

  background-color:
    var(--bg-gray-light);

  color:
    var(--text-main);
}

.confirm-button {

  background-color:
    var(--adnu-danger);

  color:
    var(--white);
}

.confirm-button:hover {

  background-color:
    var(--adnu-danger-strong);
}

</style>