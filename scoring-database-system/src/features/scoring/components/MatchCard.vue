<script setup>
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

defineProps({
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
</script>

<template>
  <article class="match-card">
    <div class="match-card__header">
      <div>
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
        :class="{
          'match-card__badge--finalized': finalized,
          'match-card__badge--pending': !finalized
        }"
      >
        {{ finalized ? game.game_status : 'Awaiting finalization' }}
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
        <span>{{ score.team }}</span>
        <span v-if="game.scoring_type === 'Threshold Incremental'">
          {{ score.sets_won }} sets won
          <template v-if="score.set_scores?.length">
            ({{ score.set_scores.join(', ') }})
          </template>
        </span>
        <span v-else-if="game.scoring_type === 'Component Score'">
          {{ score.total_score }} (weighted total)
        </span>
        <span v-else>
          {{ score.total_score }}
        </span>
        <span
          v-if="score.is_winner"
          class="winner-tag"
        >
          Winner
        </span>
      </div>
    </div>

    <PrimaryButton
      v-if="!finalized"
      class="match-card__action"
      @click="$emit('finalize')"
    >
      Finalize Match
    </PrimaryButton>
  </article>
</template>

<style scoped>
.match-card {
  background: white;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 14px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.match-card__header {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
}

.match-card__id {
  margin: 0 0 0.2rem;
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
}

.match-card__header h3 {
  margin: 0;
  font-size: 1.05rem;
}

.match-card__round {
  margin: 0.3rem 0 0;
  color: var(--text-muted);
  font-size: 0.85rem;
}

.match-card__badge {
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
}

.match-card__badge--pending {
  background: #fef3c7;
  color: #92400e;
}

.match-card__badge--finalized {
  background: #dbeafe;
  color: #1d4ed8;
}

.match-card__meta {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.match-card__teams {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.team-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  background: #f3f4f6;
  font-size: 0.8rem;
  font-weight: 600;
}

.team-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.match-card__results {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  padding-top: 0.35rem;
  border-top: 1px solid var(--border-color, #e2e8f0);
}

.result-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.winner-tag {
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: #dcfce7;
  color: #166534;
  font-size: 0.75rem;
  font-weight: 700;
}

.match-card__action {
  align-self: flex-start;
  margin-top: 0.25rem;
}
</style>
