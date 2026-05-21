<script setup>
import Navbar from '@/components/common/NavBar.vue'
import Sidebar from '@/components/common/SideBar.vue'
</script>
    
<template>
  <div class="dashboard-layout">

    <Sidebar />

    <div class="dashboard-content">
      <Navbar />

      <main class="dashboard-main">
        <slot />
      </main>
    </div>

  </div>
</template>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  background: var(--bg-gray-light);
}

.dashboard-content {
  flex: 1;
  min-width: 0;
}

.dashboard-main {
  padding: 24px;
}

@media (max-width: 860px) {
  .dashboard-layout {
    flex-direction: column;
  }

  .dashboard-main {
    padding: 16px;
  }
}
</style>
