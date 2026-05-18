<script setup>
defineProps({

  totalScores: Number,

  winnerScores: Number
})
</script>

<template>

  <div class="score-stats-grid">

    <div class="stat-card card-base">

      <p>Total Scores</p>

      <h1>
        {{ totalScores }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Winner Records</p>

      <h1>
        {{ winnerScores }}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.score-stats-grid {
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