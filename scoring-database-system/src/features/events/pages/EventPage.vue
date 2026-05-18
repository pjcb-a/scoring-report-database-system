<script setup>
import { onMounted, ref } from 'vue'

import Modal from '@/components/common/Modal.vue'

import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

import EventForm from '../components/EventForm.vue'
import EventHeader from '../components/EventHeader.vue'
import EventStats from '../components/EventStats.vue'
import EventTable from '../components/EventTable.vue'
import EventEmptyState from '../components/EventEmptyState.vue'

import {
  useEventStore
} from '../store/eventStore'


const openModal = ref(false)


const {

  events,

  loading,

  totalEvents,

  activeEvents,

  loadEvents,

  addEvent

} = useEventStore()


const handleCreateEvent = async (
  payload
) => {

  await addEvent(payload)

  openModal.value = false
}


onMounted(() => {

  loadEvents()
})
</script>

<template>

  <div class="event-page">

    <EventHeader
      @add="openModal = true"
    />

    <EventStats
      :total-events="totalEvents"
      :active-events="activeEvents"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <EventTable
      v-else-if="events.length"
      :events="events"
    />

    <EventEmptyState
      v-else
    />

    <Modal
      :is-open="openModal"
      title="Create Event"
      @close="openModal = false"
    >

      <EventForm
        @submit="handleCreateEvent"
      />

    </Modal>

  </div>

</template>

<style scoped>
.event-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
</style>