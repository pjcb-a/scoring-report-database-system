<script setup>
defineProps({

  totalGames: Number,

  activeGames: Number
})
</script>

<template>

  <div class="game-stats-grid">

    <div class="stat-card card-base">

      <p>Total Games</p>

      <h1>
        {{ totalGames }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Ongoing Games</p>

      <h1>
        {{ activeGames }}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.game-stats-grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-card h1 {
  font-size: 40px;
  color: var(--adnu-blue-dark);
}
</style>