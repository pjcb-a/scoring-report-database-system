<script setup>
defineProps({

  scores: {
    type: Array,
    required: true
  }
})
</script>

<template>

  <div class="card-base">

    <div class="section-header">

      <h2>
        Recent Winners
      </h2>

    </div>

    <div
      v-if="scores.length"
      class="scores-list"
    >

      <div
        v-for="score in scores"
        :key="score.game_score_id"
        class="score-item"
      >

        <div>

          <h3>
            {{ score.team }}
          </h3>

          <p>
            Score:
            {{ score.score_value }}
          </p>

        </div>

        <span class="winner-badge">
          Winner
        </span>

      </div>

    </div>

    <p v-else>
      No winners recorded yet.
    </p>

  </div>

</template>

<style scoped>
.section-header {
  margin-bottom: 20px;
}

.scores-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.score-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding-bottom: 12px;

  border-bottom:
    1px solid var(--border-color);
}

.winner-badge {
  color: green;
  font-weight: 600;
}
</style>