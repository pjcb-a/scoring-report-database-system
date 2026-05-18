<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  sport: {
    type: Object,
    required: true
  }
})
</script>


<template>

  <div class="sport-card card-base">

    <div class="sport-top">

      <h2>
        {{ sport.sport_name }}
      </h2>

      <Badge variant="primary">
        {{ sport.scoring_type }}
      </Badge>

    </div>

  </div>

</template>

<style scoped>
.sport-card {
  display: flex;
  flex-direction: column;
}

.sport-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>