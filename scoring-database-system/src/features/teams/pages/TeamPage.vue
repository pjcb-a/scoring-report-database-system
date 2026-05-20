<script setup>
import { onMounted, ref } from 'vue'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import TeamHeader from '../components/TeamHeader.vue'
import TeamStats from '../components/TeamStats.vue'
import TeamTable from '../components/TeamTable.vue'
import TeamForm from '../components/TeamForm.vue'
import TeamEmptyState from '../components/TeamEmptyState.vue'

import {
  useTeamStore
} from '../store/teamStore'

const openModal = ref(false)

const {

  teams,

  loading,

  totalTeams,

  loadTeams,

  addTeam

} = useTeamStore()

const handleCreateTeam = async (
  payload
) => {

  await addTeam(payload)

  openModal.value = false
}

onMounted(async () => {

  await loadTeams()
})
</script>

<template>

  <div class="teams-page">

    <TeamHeader
      @add="openModal = true"
    />

    <TeamStats
      :total-teams="totalTeams"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <TeamTable
      v-else-if="teams.length"
      :teams="teams"
    />

    <TeamEmptyState
      v-else
    />

    <Modal
      :is-open="openModal"
      title="Create Team"
      @close="openModal = false"
    >

      <TeamForm
        @submit="handleCreateTeam"
      />

    </Modal>

  </div>

</template>

<style scoped>
.teams-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>

