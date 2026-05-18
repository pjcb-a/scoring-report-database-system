<script setup>
defineProps({

  games: {
    type: Array,
    required: true
  }
})
</script>

<template>

  <div class="card-base">

    <div class="section-header">

      <h2>
        Recent Games
      </h2>

    </div>

    <div
      v-if="games.length"
      class="games-list"
    >

      <div
        v-for="game in games"
        :key="game.game_id"
        class="game-item"
      >

        <div>

          <h3>
            {{ game.event }}
            -
            {{ game.sport }}
          </h3>

          <p>
            {{ game.round }}
          </p>

        </div>

        <span class="status">
          {{ game.status }}
        </span>

      </div>

    </div>

    <p v-else>
      No recent games found.
    </p>

  </div>

</template>

<style scoped>
.section-header {
  margin-bottom: 20px;
}

.games-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.game-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding-bottom: 12px;

  border-bottom:
    1px solid var(--border-color);
}

.status {
  font-size: 14px;
  color: var(--text-muted);
}
</style>