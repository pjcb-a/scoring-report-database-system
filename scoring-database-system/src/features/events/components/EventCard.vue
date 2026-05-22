<script setup>
import { useRouter } from 'vue-router'
import {
  eventStatusBadgeClass,
  normalizeEventStatus
} from '../utils/eventStatus'

const router = useRouter()

const props = defineProps({

  event: {
    type: Object,
    required: true
  },

  isActive: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'select',
  'edit',
  'delete'
])

/*
------------------------------------------------------------------------------
OPEN EVENT
------------------------------------------------------------------------------
*/

const openEvent = async () => {

  emit(
    'select',
    props.event
  )

  /*
  --------------------------------------------------------------------------
  OPEN EVENT WORKSPACE
  --------------------------------------------------------------------------
  */

  await router.push(

    `/events/${props.event.event_id}/dashboard`
  )
}

/*
------------------------------------------------------------------------------
DELETE EVENT
------------------------------------------------------------------------------
*/

const editEvent = () => {
  emit('edit', props.event)
}

const deleteEvent = () => {

  const confirmed = window.confirm(

    `Delete "${props.event.event_name}"?`
  )

  if (!confirmed) {
    return
  }

  emit(
    'delete',
    props.event.event_id
  )
}
</script>

<template>
  <div

    class="event-card"

    :class="{
      'active-event-card':
        isActive
    }"
  >

    <!-- HEADER -->

    <div class="event-card-header">

      <div>
        <h2>
          {{ event.event_name }}
        </h2>

        <p class="event-status-label">
          {{ normalizeEventStatus(event.status) }}
        </p>
      </div>

      <div
        class="event-status-badge"
        :class="eventStatusBadgeClass(event.status)"
      >
        {{ normalizeEventStatus(event.status) }}
      </div>
    </div>

    <!-- DETAILS -->

    <div class="event-details">

      <div class="detail-item">

        <i class="fa-solid fa-calendar"></i>

        <span>
          {{ event.start_day }}
        </span>
      </div>

      <div class="detail-item">

        <i class="fa-solid fa-calendar-check"></i>

        <span>
          {{ event.end_day }}
        </span>
      </div>
    </div>

    <!-- STATS -->

    <div class="event-stats">

      <div class="stat-card">

        <strong>
          {{ event.total_sports || 0 }}
        </strong>

        <span>
          Sports
        </span>
      </div>

      <div class="stat-card">

        <strong>
          {{ event.total_teams || 0 }}
        </strong>

        <span>
          Teams
        </span>
      </div>

      <div class="stat-card">

        <strong>
          {{ event.total_games || 0 }}
        </strong>

        <span>
          Games
        </span>
      </div>
    </div>

    <!-- ACTIONS -->

    <div class="event-actions">
      <button
        type="button"
        class="edit-event-btn"
        @click="editEvent"
      >
        <i class="fa-solid fa-pen" />
        Edit
      </button>

      <button
        type="button"
        class="open-event-btn"
        @click="openEvent"
      >
        <i class="fa-solid fa-folder-open"></i>

        {{

          isActive

            ? 'Current Event'

            : 'Open Event'
        }}
      </button>

      <button
        type="button"
        class="delete-event-btn"
        @click="deleteEvent"
      >
        <i class="fa-solid fa-trash"></i>

        Delete
      </button>
    </div>
  </div>
</template>

<style scoped>
.event-card {

  display: flex;

  flex-direction: column;

  gap: 1rem;

  padding: 1.25rem;

  border-radius: 16px;

  background: white;

  border: 1px solid #e5e7eb;

  transition: 0.2s ease;
}

.active-event-card {

  border: 2px solid #2563eb;

  box-shadow:
    0 10px 30px rgba(
      37,
      99,
      235,
      0.18
    );
}

.event-card-header {

  display: flex;

  align-items: flex-start;

  justify-content: space-between;
}

.event-card-header h2 {

  margin: 0;

  font-size: 1.1rem;
}

.event-card-header p {

  margin-top: 0.25rem;

  color: #6b7280;
}

.event-status-label {
  margin-top: 0.25rem;
  color: #6b7280;
}

.event-status-badge {
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-badge--upcoming {
  background: #fef3c7;
  color: #92400e;
}

.status-badge--ongoing {
  background: #dbeafe;
  color: #1d4ed8;
}

.status-badge--completed {
  background: #dcfce7;
  color: #166534;
}

.event-details {

  display: flex;

  flex-direction: column;

  gap: 0.75rem;
}

.detail-item {

  display: flex;

  align-items: center;

  gap: 0.6rem;

  color: #4b5563;
}

.event-stats {

  display: grid;

  grid-template-columns:
    repeat(3, 1fr);

  gap: 0.75rem;
}

.stat-card {

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;

  padding: 0.8rem;

  border-radius: 12px;

  background: #f9fafb;
}

.event-actions {

  display: flex;

  justify-content: flex-end;

  gap: 0.75rem;
}

.edit-event-btn,
.open-event-btn,
.delete-event-btn {

  display: flex;

  align-items: center;

  gap: 0.5rem;

  padding: 0.8rem 1rem;

  border: none;

  border-radius: 10px;

  color: white;

  cursor: pointer;

  transition: 0.2s ease;
}

.edit-event-btn {
  margin-right: auto;
  background: #eff6ff;
  color: #1d4ed8;
}

.edit-event-btn:hover {
  background: #dbeafe;
}

.open-event-btn {
  background: #2563eb;
}

.open-event-btn:hover {

  background: #1d4ed8;
}

.delete-event-btn {

  background: #dc2626;
}

.delete-event-btn:hover {

  background: #b91c1c;
}
</style>