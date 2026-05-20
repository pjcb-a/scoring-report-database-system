<script setup>
</script>

<template>

  <aside class="sidebar">

    <div class="sidebar-header">

      <h1 class="sidebar-logo">
        NIGGA
      </h1>

      <p class="sidebar-subtitle">
        Sports Reporting
      </p>

    </div>

    <nav class="sidebar-nav">

      <router-link
        to="/"
        class="sidebar-link"
      >
        Dashboard
      </router-link>

      <router-link
        to="/events"
        class="sidebar-link"
      >
        Events
      </router-link>

      <router-link
        to="/sports"
        class="sidebar-link"
      >
        Sports
      </router-link>

      <router-link
        to="/teams"
        class="sidebar-link"
      >
        Teams
      </router-link>

      <router-link
        to="/games"
        class="sidebar-link"
      >
        Games
      </router-link>

      <router-link
        to="/scoring"
        class="sidebar-link"
      >
        Scoring
      </router-link>

      <router-link
        to="/judging"
        class="sidebar-link"
      >
        Judging
      </router-link>

      <router-link
        to="/reports"
        class="sidebar-link"
      >
        Reports
      </router-link>

    </nav>

  </aside>

</template>

<style scoped>
.sidebar {
  width: 260px;
  min-height: 100vh;

  background-color: var(--adnu-blue-dark);

  border-right: 1px solid var(--border-color);

  padding: 20px;
  border-radius: 0 15px 15px 0;
}

.sidebar-header {
  margin-bottom: 30px;
}

.sidebar-logo {
  font-size: 28px;
  font-weight: 800;
  color: var(--adnu-danger-light);
}

.sidebar-subtitle {
  color: var(--text-muted);
  font-size: 13px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
  color: var(--adnu-blue-light);
}

.sidebar-link {
  padding: 12px 16px;

  border-radius: var(--radius-md);

  transition: var(--transition-fast);

  color: var(--text-main);
}

.sidebar-link:hover {
  background-color: var(--adnu-blue-light);
}

.sidebar-link.router-link-active {
  background-color: var(--adnu-blue-dark);
  color: var(--white);
}
</style>
