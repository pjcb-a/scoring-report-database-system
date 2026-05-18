<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  score: {
    type: Object,
    required: true
  }
})
</script>

<template>

  <div class="score-card card-base">

    <div class="score-top">

      <div>

        <h2>
          {{ score.team }}
        </h2>

        <p>
          Score:
          {{ score.score_value }}
        </p>

      </div>

      <Badge
        :variant="
          score.isWinner
            ? 'success'
            : 'primary'
        "
      >
        {{
          score.isWinner
            ? 'Winner'
            : 'Participant'
        }}
      </Badge>

    </div>

  </div>

</template>

<style scoped>
.score-card {
  display: flex;
  flex-direction: column;
}

.score-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>