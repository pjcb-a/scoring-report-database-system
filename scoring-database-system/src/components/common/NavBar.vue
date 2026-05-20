<script setup>
</script>

<template>

  <header class="navbar">

    <div class="navbar-left">
      <h2 class="system-title">
        Sports Reporting Database System
      </h2>
    </div>

    <div class="navbar-right">

      <div class="badge-gold">
        ADMIN
      </div>

    </div>

  </header>

</template>

<style scoped>
header {
  padding: 35px;
}
.navbar {
  height: 72px;

  background-color: var(--white);

  border-bottom: 1px solid var(--border-color);

  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 0 24px;
}

.system-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--adnu-blue-dark);
}
</style>
