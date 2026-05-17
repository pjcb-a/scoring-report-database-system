<template>

  <aside class="w-64 bg-white border-r min-h-screen p-4">

    <h1 class="text-xl font-bold mb-8">
      Sports Reporting System
    </h1>

    <nav class="flex flex-col gap-2">

      <router-link to="/" class="btn-ghost">
        Dashboard
      </router-link>

      <router-link to="/events" class="btn-ghost">
        Events
      </router-link>

      <router-link to="/sports" class="btn-ghost">
        Sports
      </router-link>

      <router-link to="/teams" class="btn-ghost">
        Teams
      </router-link>

      <router-link to="/games" class="btn-ghost">
        Games
      </router-link>

      <router-link to="/reports" class="btn-ghost">
        Reports
      </router-link>

    </nav>

  </aside>

</template>