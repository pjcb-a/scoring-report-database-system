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
    rgba(0, 0, 0, 0.4);

  display: flex;

  align-items: center;

  justify-content: center;

  z-index: 9999;
}

.dialog-card {

  width: 420px;

  background-color: white;

  border-radius: 16px;

  padding: 28px;

  box-shadow:
    0 20px 40px rgba(
      0,
      0,
      0,
      0.2
    );
}

.dialog-title {

  font-size: 24px;

  font-weight: 700;

  margin-bottom: 14px;
}

.dialog-message {

  color: var(--text-muted);

  line-height: 1.5;
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

  border-radius: 10px;

  cursor: pointer;

  font-weight: 600;
}

.cancel-button {

  background-color:
    #e5e7eb;
}

.confirm-button {

  background-color:
    var(--adnu- );

  color: white;
}

</style>