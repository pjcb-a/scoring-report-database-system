<script setup>
</script>

<template>
  <div class="spinner-container">

    <div class="spinner"></div>

    <p class="loading-text">
      Loading...
    </p>

  </div>
</template>

<style scoped>
.spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 30px;
}

.spinner {
  width: 42px;
  height: 42px;
  border: 4px solid var(--border-color);
  border-top-color: var(--adnu-blue-dark);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-text {
  color: var(--text-muted);
  font-size: 14px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
