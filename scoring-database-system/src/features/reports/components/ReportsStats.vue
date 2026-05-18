<script setup>
defineProps({

  totalReports: Number,

  winners: Number
})
</script>

<template>

  <div class="reports-stats-grid">

    <div class="stat-card card-base">

      <p>Total Records</p>

      <h1>
        {{ totalReports }}
      </h1>

    </div>

    <div class="stat-card card-base">

      <p>Winner Records</p>

      <h1>
        {{ winners }}
      </h1>

    </div>

  </div>

</template>

<style scoped>
.reports-stats-grid {
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