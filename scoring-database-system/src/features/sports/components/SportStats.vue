<script setup>
defineProps({

  totalSports: Number,

  componentSports: Number
})
</script>

<template>

  <div class="sport-stats-grid">

    <div class="stat-card card-base">

      <p>Total Sports</p>

      <h1>
        {{ totalSports  || 0}}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Component Sports</p>

      <h1>
        {{ componentSports || 0}}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.sport-stats-grid {
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