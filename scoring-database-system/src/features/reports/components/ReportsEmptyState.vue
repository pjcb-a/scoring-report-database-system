<script setup>
</script>

<template>

  <div class="empty-state card-base">

      <div class="empty-icon">

        <i class="fa-solid fa-chalkboard-user"></i>

      </div>

    <h2>
      No Reports Available
    </h2>

    <p>
      Reports will appear once
      games and scores are recorded.
    </p>

  </div>

</template>

<style scoped>
.empty-state {
  padding: 40px;
  text-align: center;
}

.empty-state p {
  margin-top: 10px;
  color: var(--text-muted);
}

.empty-state h2 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--adnu-blue-dark);
}

.empty-icon {
  font-size: 64px;
  color: var(--adnu-blue-dark);
  margin-bottom: 20px;
}
</style>