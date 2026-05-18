<script setup>
import { onMounted, ref } from 'vue'

import Modal from '@/components/common/Modal.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import GameHeader from '../components/GameHeader.vue'
import GameStats from '../components/GameStats.vue'
import GameTable from '../components/GameTable.vue'
import GameForm from '../components/GameForm.vue'
import GameEmptyState from '../components/GameEmptyState.vue'

import {
  useGameStore
} from '../store/gameStore'

const openModal = ref(false)

const {

  games,

  eventSports,

  loading,

  totalGames,

  activeGames,

  loadGames,

  loadEventSports,

  addGame

} = useGameStore()

const handleCreateGame = async (
  payload
) => {

  await addGame(payload)

  openModal.value = false
}

onMounted(async () => {

  await loadGames()

  await loadEventSports()
})
</script>

<template>

  <div class="games-page">

    <GameHeader
      @add="openModal = true"
    />

    <GameStats
      :total-games="totalGames"
      :active-games="activeGames"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <GameTable
      v-else-if="games.length"
      :games="games"
    />

    <GameEmptyState
      v-else
    />

    <Modal
      :is-open="openModal"
      title="Create Game"
      @close="openModal = false"
    >

      <GameForm
        :event-sports="eventSports"
        @submit="handleCreateGame"
      />

    </Modal>

  </div>

</template>

<style scoped>
.games-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>