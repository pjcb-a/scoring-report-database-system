<script setup>
  defineProps({
    totalEvents: Number,
    activeEvents: Number
  })
</script>

<template>

  <div class="event-stats-grid">

    <div class="card-base stat-card">

      <p>Total Events</p>

      <h1>
        {{ totalEvents }}
      </h1>

    </div>

    <div class="card-base stat-card">

      <p>Active Events</p>

      <h1>
        {{ activeEvents }}
      </h1>

    </div>

  </div>

</template>


<style scoped>
.event-stats-grid {
  display: grid;

  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;
}

.stat-card h1 {
  margin-top: 10px;

  font-size: 36px;

  color: var(--adnu-blue-dark);
}
</style>