<script setup>
defineProps({

  judgeScore: {
    type: Object,
    required: true
  }
})
</script>

<template>

  <div class="judge-score-card card-base">

    <div class="judge-score-top">

      <div>

        <h2>
          {{ judgeScore.team }}
        </h2>

        <p>
          {{ judgeScore.criteria }}
        </p>

      </div>

      <div class="score-value">

        {{ judgeScore.score_value }}

      </div>

    </div>

  </div>

</template>

<style scoped>
.judge-score-card {
  display: flex;
  flex-direction: column;
}

.judge-score-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.score-value {
  font-size: 24px;
  font-weight: 700;

  color: var(--adnu-blue-dark);
}
</style>