<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  game: {
    type: Object,
    required: true
  }
})
</script>

<template>

  <div class="game-card card-base">

    <div class="game-top">

      <div>

        <h2>
          {{ game.event }}
          -
          {{ game.sport }}
        </h2>

        <p>
          {{ game.round }}
        </p>

      </div>

      <Badge
        :variant="
          game.status === 'Completed'
            ? 'primary'
            : game.status === 'Ongoing'
            ? 'success'
            : 'warning'
        "
      >
        {{ game.status }}
      </Badge>

    </div>

  </div>

</template>

<style scoped>
.game-card {
  display: flex;
  flex-direction: column;
}

.game-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>