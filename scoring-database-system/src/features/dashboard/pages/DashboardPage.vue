<script setup>
import { onMounted } from 'vue'

import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import DashboardHeader from '../components/DashboardHeader.vue'
import DashboardStats from '../components/DashboardStats.vue'
import RecentGames from '../components/RecentGames.vue'
import RecentScores from '../components/RecentScores.vue'
import QuickActions from '../components/QuickActions.vue'
import DashboardEmptyState from '../components/DashboardEmptyState.vue'

import {
  useDashboardStore
} from '../store/dashboardStore'


const {

  loading,

  totalEvents,

  totalSports,

  totalGames,

  totalScores,

  recentGames,

  recentWinners,

  loadDashboard

} = useDashboardStore()


onMounted(async () => {

  await loadDashboard()
})
</script>

<template>

  <div class="dashboard-page">

    <DashboardHeader />

    <LoadingSpinner
      v-if="loading"
    />

    <template v-else>

      <DashboardStats
        v-if="
          totalEvents ||
          totalSports ||
          totalGames ||
          totalScores
        "
        :total-events="totalEvents"
        :total-sports="totalSports"
        :total-games="totalGames"
        :total-scores="totalScores"
      />

      <div
        v-if="
          recentGames.length ||
          recentWinners.length
        "
        class="dashboard-grid"
      >

        <RecentGames
          :games="recentGames"
        />

        <RecentScores
          :scores="recentWinners"
        />

        <QuickActions />

      </div>

      <DashboardEmptyState
        v-else
      />

    </template>

  </div>

</template>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;

  gap: 24px;
}

.dashboard-grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(320px, 1fr));

  gap: 20px;
}
</style>