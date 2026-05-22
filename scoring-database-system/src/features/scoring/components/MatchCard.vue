<script setup>
import { computed } from 'vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import { formatScore } from '@/utils/formatters'

const props = defineProps({
  game: {
    type: Object,
    required: true
  },
  finalized: {
    type: Boolean,
    default: false
  }
})

defineEmits(['finalize'])

const statusBadgeClass = computed(() => {
  if (!props.finalized) {
    return 'match-card__badge--pending'
  }

  const status = (props.game.game_status || '').toLowerCase()

  if (status === 'win') {
    return 'match-card__badge--win'
  }

  if (status === 'forfeit') {
    return 'match-card__badge--forfeit'
  }

  return 'match-card__badge--finalized'
})

const statusLabel = computed(() => {
  if (!props.finalized) {
    return 'Awaiting finalization'
  }

  return props.game.game_status || 'Finalized'
})
</script>

<template>
  <article
    class="match-card"
    :class="{ 'match-card--finalized': finalized }"
  >
    <div class="match-card__header">
      <div class="match-card__title-block">
        <p class="match-card__id">
          Game #{{ game.game_id }}
        </p>
        <h3>{{ game.sport || game.game_name }}</h3>
        <p
          v-if="game.round"
          class="match-card__round"
        >
          {{ game.round }}
        </p>
      </div>

      <span
        class="match-card__badge"
        :class="statusBadgeClass"
      >
        {{ statusLabel }}
      </span>
    </div>

    <div class="match-card__meta">
      <span>{{ game.scoring_type }}</span>
      <span v-if="game.set_count">
        · {{ game.set_count }} sets
      </span>
    </div>

    <div
      v-if="game.teams?.length"
      class="match-card__teams"
    >
      <span
        v-for="team in game.teams"
        :key="team.team_id"
        class="team-chip"
      >
        <span
          class="team-dot"
          :style="{ backgroundColor: team.team_color }"
        />
        {{ team.team_name }}
      </span>
    </div>

    <div
      v-if="finalized && game.scores?.length"
      class="match-card__results"
    >
      <div
        v-for="score in game.scores"
        :key="score.game_score_id"
        class="result-row"
      >
        <span class="result-row__team">{{ score.team }}</span>

        <span class="result-row__score">
          <template v-if="game.scoring_type === 'Threshold Incremental'">
            {{ score.sets_won }} sets won
            <template v-if="score.set_scores?.length">
              ({{ score.set_scores.join(', ') }})
            </template>
          </template>
          <template v-else-if="game.scoring_type === 'Component Score'">
            {{ formatScore(score.total_score) }} (weighted total)
          </template>
          <template v-else>
            {{ score.total_score }}
          </template>
        </span>

        <span
          v-if="score.is_winner"
          class="winner-tag"
        >
          Winner
        </span>
        <span
          v-else
          class="result-row__spacer"
        />
      </div>
    </div>

    <div
      v-if="!finalized"
      class="match-card__footer"
    >
      <PrimaryButton
        class="match-card__action"
        label="Finalize Match"
        @click="$emit('finalize')"
      />
    </div>
  </article>
</template>

<style scoped>
.match-card {
  background: white;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  height: 100%;
}

.match-card--finalized {
  gap: 12px;
}

.match-card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.match-card__title-block {
  min-width: 0;
  flex: 1;
}

.match-card__id {
  margin: 0 0 4px;
  font-size: 0.75rem;
  color: var(--text-muted, #64748b);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.match-card__header h3 {
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.35;
}

.match-card__round {
  margin: 6px 0 0;
  color: var(--text-muted, #64748b);
  font-size: 0.85rem;
  line-height: 1.4;
}

.match-card__badge {
  flex-shrink: 0;
  align-self: flex-start;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
  line-height: 1.3;
  text-align: center;
  max-width: 9.5rem;
}

.match-card__badge--pending {
  background: #fef3c7;
  color: #92400e;
}

.match-card__badge--win {
  background: #dcfce7;
  color: #166534;
}

.match-card__badge--forfeit {
  background: #fee2e2;
  color: #991b1b;
}

.match-card__badge--finalized {
  background: #dbeafe;
  color: #1d4ed8;
}

.match-card__meta {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
  line-height: 1.4;
}

.match-card__teams {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0;
}

.team-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 999px;
  background: #f3f4f6;
  font-size: 0.8rem;
  font-weight: 600;
}

.team-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.match-card__results {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin: 4px 0 0;
  padding-top: 14px;
  border-top: 1px solid var(--border-color, #e2e8f0);
}

.result-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  align-items: center;
  gap: 12px 16px;
  padding: 12px 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.result-row:not(:last-child) {
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.result-row__team {
  font-weight: 600;
  color: var(--text-main, #1e293b);
}

.result-row__score {
  color: var(--text-muted, #64748b);
  text-align: right;
  white-space: nowrap;
}

.result-row__spacer {
  width: 52px;
}

.winner-tag {
  justify-self: end;
  padding: 4px 10px;
  border-radius: 999px;
  background: #dcfce7;
  color: #166534;
  font-size: 0.72rem;
  font-weight: 700;
  white-space: nowrap;
}

.match-card__footer {
  margin-top: auto;
  padding-top: 6px;
}

.match-card__action {
  width: 100%;
}

.match-card__action :deep(.primary-button) {
  width: 100%;
}
</style>
