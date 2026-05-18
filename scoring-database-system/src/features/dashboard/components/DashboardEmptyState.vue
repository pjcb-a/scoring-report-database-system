<script setup>
</script>

<template>

  <div class="dashboard-empty-state card-base">

    <div class="empty-content">

      <div class="empty-icon">

        📊

      </div>

      <h2>
        No Dashboard Data Available
      </h2>

      <p>
        There are currently no events, games,
        scores, or reports available in the system.
      </p>

      <p class="sub-message">
        Start by creating an event or adding
        sports competitions to populate the dashboard.
      </p>

    </div>

  </div>

</template>

<style scoped>
.dashboard-empty-state {
  display: flex;
  justify-content: center;
  align-items: center;

  min-height: 320px;

  padding: 40px;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;

  text-align: center;

  max-width: 500px;
}

.empty-icon {
  font-size: 64px;

  margin-bottom: 20px;
}

.empty-content h2 {
  font-size: 28px;
  font-weight: 700;

  margin-bottom: 12px;

  color: var(--adnu-blue-dark);
}

.empty-content p {
  font-size: 15px;
  line-height: 1.6;

  color: var(--text-muted);
}

.sub-message {
  margin-top: 10px;
  font-size: 14px;
}
</style>