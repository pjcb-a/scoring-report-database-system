<script setup>
import { onMounted, ref } from 'vue'

import Card from '@/components/ui/Card.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

import { getEvents } from '../services/eventService'

    const events = ref([])

    const loadEvents = async () => {
    events.value = await getEvents()
    }

    onMounted(() => {
    loadEvents()
    })
</script>

<template>

  <div>

    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Events</h1>

      <PrimaryButton>
        Add Event
      </PrimaryButton>
    </div>

    <Card>

      <table class="w-full">
        <thead>
          <tr>
            <th class="text-left py-2">Event Name</th>
            <th class="text-left py-2">Status</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="event in events"
            :key="event.event_id"
          >
            <td class="py-3">
              {{ event.event_name }}
            </td>

            <td>
              {{ event.status }}
            </td>
          </tr>
        </tbody>
      </table>

    </Card>

  </div>

</template>

<style scoped>

.event-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

</style>