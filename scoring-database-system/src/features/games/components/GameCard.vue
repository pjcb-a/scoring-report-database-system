<script setup>

defineProps({

  game: {
    type: Object,
    required: true
  }
})

const formatDateTime =
  (value) => {

    if (!value) {
      return '—'
    }

    const date =
      new Date(value)

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
          {{ game.sport || game.game_name }}
        </h3>

        <p
          v-if="game.round"
          class="game-meta"
        >
          {{ game.round }}
        </p>

      </div>

      <span class="game-status-badge">
        {{ game.game_status }}
      </span>

    </div>

    <div class="game-details">

      <div class="game-detail-item">

        <i class="fa-solid fa-location-dot"></i>

        <span>
          {{ game.venue_name || 'No venue' }}
        </span>

      </div>

      <div class="game-detail-item">

        <i class="fa-solid fa-clock"></i>

        <span>
          {{ formatDateTime(game.start_date) }}
        </span>

      </div>

      <div
        v-if="game.end_date"
        class="game-detail-item"
      >

        <i class="fa-solid fa-clock-rotate-left"></i>

        <span>
          {{ formatDateTime(game.end_date) }}
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
            :style="{
              backgroundColor:
                team.team_color
            }"
          />
          {{ team.team_name }}
        </span>

      </div>

    </div>

  </div>

</template>

<style scoped>

.game-card {

  background-color: white;

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  padding: 1.25rem;

  transition: 0.2s ease;
}

.game-card:hover {

  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.08);

  transform: translateY(-1px);
}

.game-card-header {

  display: flex;

  align-items: flex-start;

  justify-content: space-between;

  gap: 0.75rem;

  margin-bottom: 1rem;
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

  background: #dbeafe;

  color: #1d4ed8;

  font-size: 0.75rem;

  font-weight: 600;

  white-space: nowrap;
}

.game-details {

  display: flex;

  flex-direction: column;

  gap: 0.6rem;
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

  border:
    1px solid rgba(0, 0, 0, 0.1);
}

</style>
