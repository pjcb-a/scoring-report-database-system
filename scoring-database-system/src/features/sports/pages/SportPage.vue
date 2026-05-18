<script setup>
import { onMounted, ref } from 'vue'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import SportHeader from '../components/SportHeader.vue'
import SportStats from '../components/SportStats.vue'
import SportTable from '../components/SportTable.vue'
import SportForm from '../components/SportForm.vue'
import SportEmptyState from '../components/SportEmptyState.vue'

import { useSportStore } from '../store/sportStore'

const openModal = ref(false)

const {

  sports,

  scoringTypes,

  loading,

  totalSports,

  componentSports,

  loadSports,

  loadScoringTypes,

  addSport

} = useSportStore()

const handleCreateSport = async (
  payload
) => {

  await addSport(payload)

  openModal.value = false
}

onMounted(async () => {

  await loadSports()

  await loadScoringTypes()
})
</script>

<template>

  <div class="sports-page">

    <SportHeader
      @add="openModal = true"
    />

    <SportStats
      :total-sports="totalSports"
      :component-sports="componentSports"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <SportTable
      v-else-if="sports.length"
      :sports="sports"
    />

    <SportEmptyState
      v-else
    />

    <Modal
      :is-open="openModal"
      title="Create Sport"
      @close="openModal = false"
    >

      <SportForm
        :scoring-types="scoringTypes"
        @submit="handleCreateSport"
      />

    </Modal>

  </div>

</template>

<style scoped>
.sports-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>