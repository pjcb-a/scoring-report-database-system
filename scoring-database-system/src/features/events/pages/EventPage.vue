<script setup>
  import { onMounted, ref } from 'vue'
  
  import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
  import Modal from '@/components/common/Modal.vue'
  
  import PrimaryButton from '@/components/ui/PrimaryButton.vue'
  
  import EventForm from '../components/EventForm.vue'
  import EventStats from '../components/EventStats.vue'
  import EventTable from '../components/EventTable.vue'
  
  import {
    useEventStore
  } from '../store/eventStore'
  
  const openModal = ref(false)
  
  const {
    events,
    loading,
  
    totalEvents,
    activeEvents,
  
    fetchEvents,
    addEvent
  } = useEventStore()
  
  const handleCreateEvent = async (
    payload
  ) => {
  
    await addEvent(payload)
  
    openModal.value = false
  }
  
  onMounted(() => {
    fetchEvents()
  })
</script>

<template>

  <div class="event-page">

    <div class="page-header">

      <div>
        <h1>Events</h1>

        <p>
          Manage sports events and activities.
        </p>
      </div>

      <PrimaryButton
        @click="openModal = true"
      >
        Add Event
      </PrimaryButton>

    </div>

    <EventStats
      :total-events="totalEvents"
      :active-events="activeEvents"
    />

    <LoadingSpinner
      v-if="loading"
    />

    <EventTable
      v-else
      :events="events"
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

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header p {
  margin-top: 4px;

  color: var(--text-muted);
}
</style>