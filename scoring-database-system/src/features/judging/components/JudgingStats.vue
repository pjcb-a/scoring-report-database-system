<script setup>
defineProps({

  totalJudgeScores: Number,

  totalJudges: Number
})
</script>

<template>

  <div class="judging-stats-grid">

    <div class="stat-card card-base">

      <p>
        Total Judge Scores
      </p>

      <h1>
        {{ totalJudgeScores }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>
        Total Judges
      </p>

      <h1>
        {{ totalJudges }}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.judging-stats-grid {
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