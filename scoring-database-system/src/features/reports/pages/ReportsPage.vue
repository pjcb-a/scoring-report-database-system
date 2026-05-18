<script setup>
import { onMounted } from 'vue'

import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import ReportsHeader from '../components/ReportsHeader.vue'
import ReportsStats from '../components/ReportsStats.vue'
import ReportsTable from '../components/ReportsTable.vue'
import ReportsEmptyState from '../components/ReportsEmptyState.vue'

import {
  useReportsStore
} from '../store/reportsStore'

const {

  reports,

  loading,

  totalReports,

  winners,

  loadReports

} = useReportsStore()

onMounted(async () => {

  await loadReports()
})
</script>

<template>

  <div class="reports-page">

    <ReportsHeader />

    <ReportsStats
      :total-reports="totalReports"
      :winners="winners"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <ReportsTable
      v-else-if="reports.length"
      :reports="reports"
    />

    <ReportsEmptyState
      v-else
    />

  </div>

</template>

<style scoped>
.reports-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>