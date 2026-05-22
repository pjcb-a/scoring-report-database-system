<script setup>
import { onActivated, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { useReportStore } from '../store/reportsStore'
import ReportsFilters from '../components/ReportsFilters.vue'
import ReportsSortBar from '../components/ReportsSortBar.vue'
import MatchReportCard from '../components/MatchReportCard.vue'

const router = useRouter()
const eventContextStore = useEventContextStore()
const { currentEvent } = storeToRefs(eventContextStore)

const reportStore = useReportStore()
const {
  matches,
  loading,
  error,
  displayedMatches
} = storeToRefs(reportStore)

const { loadMatchReports } = reportStore

const ensureReportsLoaded = async () => {
  if (!currentEvent.value) {
    router.push('/events')
    return
  }

  await loadMatchReports()
}

onMounted(ensureReportsLoaded)

onActivated(ensureReportsLoaded)
</script>

<template>
  <section class="reports-page">
    <div class="reports-header">
      <h1 class="reports-title">
        Reports
      </h1>
      <p class="reports-subtitle">
        All matches finalized in Scoring or Judging. Search, sort, and filter by sport, team, or day.
      </p>
    </div>

    <div
      v-if="loading"
      class="reports-loading"
    >
      Loading reports...
    </div>

    <div
      v-else-if="error"
      class="reports-error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="!matches.length"
      class="reports-empty"
    >
      No concluded matches yet. Finalize games in the Scoring tab (other scoring types) or Judging tab (Component Score).
    </div>

    <div
      v-else
      class="reports-layout"
    >
      <ReportsFilters />

      <div class="reports-main">
        <ReportsSortBar />

        <div
          v-if="!displayedMatches.length"
          class="reports-empty reports-empty--inline"
        >
          No matches match your search or filters. Try different keywords or checkboxes.
        </div>

        <div
          v-else
          class="reports-list"
        >
          <MatchReportCard
            v-for="match in displayedMatches"
            :key="match.game_id"
            :match="match"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.reports-page {
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.reports-header {
  margin-bottom: 0;
}

.reports-title {
  font-size: 32px;
  font-weight: 800;
  margin: 0;
}

.reports-subtitle {
  margin-top: 6px;
  color: var(--text-muted, #64748b);
  max-width: 720px;
}

.reports-loading,
.reports-error,
.reports-empty {
  padding: 30px;
  text-align: center;
  background: white;
  border-radius: 12px;
  border: 1px solid var(--border-color, #e2e8f0);
}

.reports-empty--inline {
  margin-top: 0;
}

.reports-layout {
  display: grid;
  grid-template-columns: minmax(240px, 280px) 1fr;
  gap: 20px;
  align-items: start;
}

.reports-main {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

@media (max-width: 900px) {
  .reports-layout {
    grid-template-columns: 1fr;
  }
}
</style>
