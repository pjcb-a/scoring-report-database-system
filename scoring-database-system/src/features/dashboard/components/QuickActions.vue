<script setup>
import { useRouter } from 'vue-router'

import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const router = useRouter()

const goTo = (path) => {
  router.push(path)
}
</script>

<template>

  <div class="card-base">

    <div class="section-header">

      <h2>
        Quick Actions
      </h2>

    </div>

    <div class="actions-grid">

      <PrimaryButton
        @click="goTo('/events')"
      >
        Add Event
      </PrimaryButton>

      <PrimaryButton
        @click="goTo('/sports')"
      >
        Add Sport
      </PrimaryButton>

      <PrimaryButton
        @click="goTo('/games')"
      >
        Add Game
      </PrimaryButton>

      <PrimaryButton
        @click="goTo('/scoring')"
      >
        Add Score
      </PrimaryButton>

      <PrimaryButton
        @click="goTo('/judging')"
      >
        Add Judge Score
      </PrimaryButton>

    </div>

  </div>

</template>

<style scoped>
.section-header {
  margin-bottom: 20px;
}

.actions-grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(180px, 1fr));

  gap: 16px;
}
</style>
