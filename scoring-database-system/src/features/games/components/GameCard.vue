<script setup>
defineProps({
  game: {
    type: Object,
    required: true
  }
})

defineEmits(['edit', 'delete'])

const formatDateTime = (value) => {
  if (!value) {
    return '—'
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString()
}
</script>

<template>
  <div class="game-card">
    <div class="game-card-header">
      <div>
        <p class="game-id-label">
          Game #{{ game.game_id }}
        </p>

        <h3>
          {{ game.game_name || game.sport }}
        </h3>

        <p
          v-if="game.round"
          class="game-meta"
        >
          {{ game.round }}
        </p>
      </div>

      <span class="game-status-badge game-status-badge--pending">
        Scheduled
      </span>
    </div>

    <div class="game-details">
      <div class="game-detail-item">
        <i class="fa-solid fa-location-dot" />
        <span>{{ game.venue_name || 'No venue' }}</span>
      </div>

      <div class="game-detail-item">
        <i class="fa-solid fa-clock" />
        <span>{{ formatDateTime(game.start_date) }}</span>
      </div>

      <div
        v-if="game.end_date"
        class="game-detail-item"
      >
        <i class="fa-solid fa-clock-rotate-left" />
        <span>{{ formatDateTime(game.end_date) }}</span>
      </div>

      <div
        v-if="game.set_count"
        class="game-detail-item"
      >
        <i class="fa-solid fa-layer-group" />
        <span>
          {{ game.set_count }} sets
          <template v-if="game.scoring_type === 'Component Score'">
            (finalize in Judging)
          </template>
          <template v-else>
            (finalize in Scoring)
          </template>
        </span>
      </div>

      <div
        v-if="game.teams?.length"
        class="game-teams"
      >
        <span
          v-for="team in game.teams"
          :key="team.team_id"
          class="game-team-chip"
        >
          <span
            class="game-team-dot"
            :style="{ backgroundColor: team.team_color }"
          />
          {{ team.team_name }}
        </span>
      </div>
    </div>

    <div class="game-card-actions">
      <button
        type="button"
        class="action-btn action-btn--edit"
        @click="$emit('edit', game)"
      >
        <i class="fa-solid fa-pen" />
        Edit
      </button>

      <button
        type="button"
        class="action-btn action-btn--delete"
        @click="$emit('delete', game)"
      >
        <i class="fa-solid fa-trash" />
        Delete
      </button>
    </div>
  </div>
</template>

<style scoped>
.game-card {
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: 0.2s ease;
}

.game-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.game-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
}

.game-id-label {
  margin: 0 0 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.game-card-header h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 0;
}

.game-meta {
  margin-top: 0.35rem;
  font-size: 0.85rem;
  color: var(--text-muted);
}

.game-status-badge {
  padding: 0.3rem 0.7rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
}

.game-status-badge--pending {
  background: #fef3c7;
  color: #92400e;
}

.game-details {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  flex: 1;
}

.game-detail-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.9rem;
  color: #4b5563;
}

.game-teams {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.game-team-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.65rem;
  border-radius: 999px;
  background: #f3f4f6;
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
}

.game-team-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.game-card-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--border-color, #e2e8f0);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: none;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: 0.15s ease;
}

.action-btn--edit {
  margin-right: auto;
  background: #eff6ff;
  color: #1d4ed8;
}

.action-btn--edit:hover {
  background: #dbeafe;
}

.action-btn--delete {
  background: #fee2e2;
  color: #b91c1c;
}

.action-btn--delete:hover {
  background: #fecaca;
}
</style>
