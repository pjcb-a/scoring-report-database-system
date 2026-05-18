<script setup>
import { onMounted, ref } from 'vue'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import ScoringHeader from '../components/ScoringHeader.vue'
import ScoreStats from '../components/ScoreStats.vue'
import ScoreTable from '../components/ScoreTable.vue'
import ScoreForm from '../components/ScoreForm.vue'
import ScoreEmptyState from '../components/ScoreEmptyState.vue'

import {
  useScoringStore
} from '../store/scoringStore'

const openModal = ref(false)

const {

  scores,

  games,

  teams,

  loading,

  totalScores,

  winnerScores,

  loadScores,

  loadGames,

  loadTeams,

  addScore

} = useScoringStore()

const handleCreateScore = async (
  payload
) => {

  await addScore(payload)

  openModal.value = false
}

onMounted(async () => {

  await loadScores()

  await loadGames()

  await loadTeams()
})
</script>

<template>

  <div class="scoring-page">

    <ScoringHeader
      @add="openModal = true"
    />

    <ScoreStats
      :total-scores="totalScores"
      :winner-scores="winnerScores"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <ScoreTable
      v-else-if="scores.length"
      :scores="scores"
    />

    <ScoreEmptyState
      v-else
    />

    <Modal
      :is-open="openModal"
      title="Create Score"
      @close="openModal = false"
    >

      <ScoreForm
        :games="games"
        :teams="teams"
        @submit="handleCreateScore"
      />

    </Modal>

  </div>

</template>

<style scoped>
.scoring-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>