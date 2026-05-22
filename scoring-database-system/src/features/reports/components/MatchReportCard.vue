<script setup>
import { COMPONENT_SCORE, formatMatchDateTime } from '../utils/matchReportUtils'
import { formatScore } from '@/utils/formatters'

defineProps({
  match: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <article class="report-card">
    <header class="report-card__header">
      <div>
        <h2>{{ match.sport || match.game_name }}</h2>
        <p v-if="match.round">
          {{ match.round }}
        </p>
        <p class="report-date">
          {{ formatMatchDateTime(match) }}
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

    <template v-if="match.scoring_type === COMPONENT_SCORE">
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
            Total: {{ formatScore(score.total_score) }}
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
              <th>Judge</th>
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
              <td>{{ component.judge }}</td>
              <td>{{ component.criteria }}</td>
              <td>{{ component.score_value }}</td>
              <td>{{ formatScore(component.weighted_score) }}</td>
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
</template>

<style scoped>
.report-card {
  background: white;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: var(--radius-lg, 12px);
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
  color: var(--text-muted, #64748b);
}

.report-date {
  font-size: 0.85rem !important;
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
  color: var(--text-muted, #64748b);
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
  border-bottom: 1px solid var(--border-color, #e2e8f0);
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

.component-team-report:last-child {
  margin-bottom: 0;
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
