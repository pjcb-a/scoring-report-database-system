<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { useReportStore } from '../store/reportsStore'

const router = useRouter()
const eventContextStore = useEventContextStore()
const { currentEvent } = storeToRefs(eventContextStore)

const reportStore = useReportStore()
const { matches, loading, error } = storeToRefs(reportStore)
const { loadMatchReports } = reportStore

onMounted(async () => {
  if (!currentEvent.value) {
    router.push('/events')
    return
  }

  await loadMatchReports()
})
</script>

<template>
  <section class="reports-page">
    <div class="reports-header">
      <h1 class="reports-title">
        {{ currentEvent?.event_name }}
      </h1>
      <p class="reports-subtitle">
        Finalized match reports for this event
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
      No finalized matches yet. Finalize games in the Scoring tab.
    </div>

    <div
      v-else
      class="reports-list"
    >
      <article
        v-for="match in matches"
        :key="match.game_id"
        class="report-card"
      >
        <header class="report-card__header">
          <div>
            <h2>{{ match.sport || match.game_name }}</h2>
            <p v-if="match.round">
              {{ match.round }}
            </p>
          </div>
          <span class="report-status">
            {{ match.game_status }}
          </span>
        </header>

        <p class="report-meta">
          {{ match.scoring_type }}
          <span v-if="match.set_count">
            · {{ match.set_count }} sets
          </span>
        </p>

        <template v-if="match.scoring_type === 'Component Score'">
          <div
            v-for="score in match.scores"
            :key="score.game_score_id"
            class="component-team-report"
          >
            <div class="component-team-header">
              <div class="team-cell">
                <span
                  class="team-color"
                  :style="{ backgroundColor: score.team_color }"
                />
                <strong>{{ score.team }}</strong>
              </div>
              <span>
                Total: {{ score.total_score }}
                <span
                  v-if="score.is_winner"
                  class="winner-tag"
                >
                  Winner
                </span>
              </span>
            </div>

            <table
              v-if="score.score_components?.length"
              class="report-table component-table"
            >
              <thead>
                <tr>
                  <th>Criteria</th>
                  <th>Score</th>
                  <th>Weighted</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="component in score.score_components"
                  :key="component.score_component_id"
                >
                  <td>{{ component.criteria }}</td>
                  <td>{{ component.score_value }}</td>
                  <td>{{ component.weighted_score }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>

        <table
          v-else
          class="report-table"
        >
          <thead>
            <tr>
              <th>Team</th>
              <th v-if="match.scoring_type === 'Threshold Incremental'">
                Sets won
              </th>
              <th v-if="match.scoring_type === 'Threshold Incremental'">
                Set scores
              </th>
              <th v-else>
                Score
              </th>
              <th v-if="match.scoring_type === 'Ranked Timed'">
                Rank
              </th>
              <th>Outcome</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="score in match.scores"
              :key="score.game_score_id"
            >
              <td>
                <div class="team-cell">
                  <span
                    class="team-color"
                    :style="{
                      backgroundColor: score.team_color
                    }"
                  />
                  {{ score.team }}
                </div>
              </td>
              <td v-if="match.scoring_type === 'Threshold Incremental'">
                {{ score.sets_won ?? '—' }}
              </td>
              <td v-if="match.scoring_type === 'Threshold Incremental'">
                {{
                  score.set_scores?.length
                    ? score.set_scores.join(', ')
                    : '—'
                }}
              </td>
              <td v-else>
                {{ score.total_score }}
              </td>
              <td v-if="match.scoring_type === 'Ranked Timed'">
                {{ score.rank_position ?? '—' }}
              </td>
              <td>
                {{
                  score.is_winner
                    ? 'Winner'
                    : '—'
                }}
              </td>
            </tr>
          </tbody>
        </table>
      </article>
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
  color: var(--text-muted);
}

.reports-loading,
.reports-error,
.reports-empty {
  padding: 30px;
  text-align: center;
  background: white;
  border-radius: 12px;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.report-card {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
}

.report-card__header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.report-card__header h2 {
  margin: 0;
  font-size: 1.2rem;
}

.report-card__header p {
  margin: 4px 0 0;
  color: var(--text-muted);
}

.report-status {
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-size: 0.8rem;
  font-weight: 700;
  white-space: nowrap;
  height: fit-content;
}

.report-meta {
  margin: 0 0 16px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.report-table {
  width: 100%;
  border-collapse: collapse;
}

.report-table th,
.report-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.team-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.team-color {
  width: 14px;
  height: 14px;
  border-radius: 50%;
}

.component-team-report {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.component-team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.component-table {
  margin-bottom: 0;
}

.winner-tag {
  margin-left: 8px;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: #dcfce7;
  color: #166534;
  font-size: 0.75rem;
  font-weight: 700;
}
</style>
