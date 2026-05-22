<script setup>
defineProps({

  totalEvents: Number,

  totalSports: Number,

  totalGames: Number,

  totalTeams: Number
})
</script>

<template>

  <div class="dashboard-stats-grid">

    <div class="stat-card card-base">

      <p>Total Events</p>

      <h1>
        {{ totalEvents }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Total Sports</p>

      <h1>
        {{ totalSports }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Total Games</p>

      <h1>
        {{ totalGames }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Total Teams</p>

      <h1>
        {{ totalTeams }}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.dashboard-stats-grid {
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