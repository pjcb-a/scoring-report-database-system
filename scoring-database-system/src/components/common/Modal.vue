<script setup>
    defineProps({
      isOpen: {
        type: Boolean,
        default: false
      },
    
      title: {
        type: String,
        default: 'Modal'
      }
    })
    
    defineEmits(['close'])
</script>

<template>

  <div
    v-if="isOpen"
    class="modal-overlay"
  >

    <div class="modal-container">

      <div class="modal-header">

        <h2>
          {{ title }}
        </h2>

        <button
          class="close-btn"
          @click="$emit('close')"
        >
          ✕
        </button>

      </div>

      <div class="modal-content">
        <slot />
      </div>

    </div>

  </div>

</template>


<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.45);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 999;
}

.modal-container {
  width: 100%;
  max-width: 720px;

  background-color: var(--white);

  border-radius: var(--radius-lg);

  box-shadow: var(--shadow-md);

  overflow: hidden;
}

.modal-header {
  padding: 18px 22px;

  border-bottom: 1px solid var(--border-color);

  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-content {
  padding: 24px;
}

.close-btn {
  background: transparent;
  font-size: 18px;
  color: var(--text-muted);
}
</style>