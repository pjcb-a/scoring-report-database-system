<script setup>
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

defineEmits(['add'])
</script>

<template>

  <div class="page-header">

    <div>

      <h1>
        Games
      </h1>

      <p>
        Manage competition instances and schedules.
      </p>

    </div>

    <PrimaryButton
      @click="$emit('add')"
    >
      Add Game
    </PrimaryButton>

  </div>

</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header p {
  margin-top: 4px;
  color: var(--text-muted);
}
</style>