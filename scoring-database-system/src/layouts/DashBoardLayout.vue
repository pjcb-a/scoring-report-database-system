<script setup>
import Navbar from '@/components/common/Navbar.vue'
import Sidebar from '@/components/common/Sidebar.vue'
</script>
    
<template>
  <div class="min-h-screen flex bg-background">

    <Sidebar />

    <div class="flex-1">
      <Navbar />

      <main class="p-6">
        <slot />
      </main>
    </div>

  </div>
</template>
