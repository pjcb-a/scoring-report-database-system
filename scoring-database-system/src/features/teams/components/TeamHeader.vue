<script setup>
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

defineEmits(['add'])
</script>

<template>

  <div class="page-header">

    <div>

      <h1>
        Teams
      </h1>

      <p>
        Manage participating teams.
      </p>

    </div>

    <PrimaryButton
      @click="$emit('add')"
    >
      Add Team
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