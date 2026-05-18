<script setup>
defineProps({

  totalEvents: {
    type: Number,
    default: 0
  },

  activeEvents: {
    type: Number,
    default: 0
  },

  completedEvents: {
    type: Number,
    default: 0
  }
})
</script>

<template>

  <div class="event-stats-grid">

    <div class="stat-card card-base">

      <div class="stat-header">
        <p>Total Events</p>
      </div>

      <h1>
        {{ totalEvents }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <div class="stat-header">
        <p>Active Events</p>
      </div>

      <h1>
        {{ activeEvents }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <div class="stat-header">
        <p>Completed Events</p>
      </div>

      <h1>
        {{ completedEvents }}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.event-stats-grid {
  display: grid;

  grid-template-columns:
    repeat(auto-fit, minmax(220px, 1fr));

  gap: 20px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-header p {
  color: var(--text-muted);
  font-size: 14px;
}

.stat-card h1 {
  font-size: 42px;
  font-weight: 800;
  color: var(--adnu-blue-dark);
}
</style>