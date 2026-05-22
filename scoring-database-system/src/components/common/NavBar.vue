<script setup>

import { storeToRefs } from 'pinia'

import {
  useEventContextStore
} from '@/features/events/store/eventContextStore'

const eventContextStore =
  useEventContextStore()

const { currentEventName } = storeToRefs(eventContextStore)

</script>

<template>

  <header class="navbar">

    <h1 class="navbar-title">

      {{ currentEventName || 'No Event Selected' }}

    </h1>

  </header>

</template>

<style scoped>

.navbar {

  width: 100%;

  padding: 20px 30px;

  background-color: var(--white);

  border-bottom:
    1px solid var(--border-color);

  display: flex;

  align-items: center;
}

.navbar-title {

  margin: 0;

  font-size: 24px;

  font-weight: 700;

  color: var(--text-main);
}

</style>
