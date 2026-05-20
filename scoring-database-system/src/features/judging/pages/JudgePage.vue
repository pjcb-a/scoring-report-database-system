<script setup>
import { onMounted, ref } from 'vue'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import JudgingHeader from '../components/JudgingHeader.vue'
import JudgingStats from '../components/JudgingStats.vue'
import JudgeScoreTable from '../components/JudgeScoreTable.vue'
import JudgeScoreForm from '../components/JudgeScoreForm.vue'
import JudgeEmptyState from '../components/JudgeEmptyState.vue'

import {
  useJudgingStore
} from '../store/judgingStore'

const openModal = ref(false)

const {

  judgeScores,

  gameScores,

  criteria,

  judges,

  loading,

  totalJudgeScores,

  totalJudges,

  loadJudgeScores,

  loadGameScores,

  loadCriteria,

  loadJudges,

  addJudgeScore

} = useJudgingStore()

const handleCreateJudgeScore = async (
  payload
) => {

  await addJudgeScore(payload)

  openModal.value = false
}

onMounted(async () => {

  await loadJudgeScores()

  await loadGameScores()

  await loadCriteria()

  await loadJudges()
})
</script>

<template>

  <div class="judging-page">

    <JudgingHeader
      @add="openModal = true"
    />

    <JudgingStats
      :total-judge-scores="totalJudgeScores"
      :total-judges="totalJudges"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <JudgeScoreTable
      v-else-if="judgeScores.length"
      :judge-scores="judgeScores"
    />

    <JudgeEmptyState
      v-else
    />

    <Modal
      :is-open="openModal"
      title="Add Judge Score"
      @close="openModal = false"
    >

      <JudgeScoreForm
        :game-scores="gameScores"
        :criteria="criteria"
        :judges="judges"
        @submit="handleCreateJudgeScore"
      />

    </Modal>

  </div>

</template>

<style scoped>
.judging-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>
