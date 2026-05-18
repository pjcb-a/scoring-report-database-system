<script setup>
import { computed } from 'vue'

import Badge from '@/components/ui/Badge.vue'

const props = defineProps({

  event: {
    type: Object,
    required: true
  }
})

const badgeVariant = computed(() => {

  switch (props.event.status) {

    case 'Active':
      return 'success'

    case 'Completed':
      return 'primary'

    default:
      return 'warning'
  }
})

const formatDate = (date) => {

  if (!date) return 'N/A'

  return new Date(date)
    .toLocaleDateString()
}
</script>

<template>

  <div class="event-card card-base">

    <div class="event-card-top">

      <div>

        <h2 class="event-title">
          {{ event.event_name }}
        </h2>

        <p class="event-date">

          {{ formatDate(event.start_day) }}

          -

          {{ formatDate(event.end_day) }}

        </p>

      </div>

      <Badge
        :variant="badgeVariant"
      >
        {{ event.status }}
      </Badge>

    </div>

    <div class="event-card-footer">

      <div class="event-meta">

        <span class="meta-label">
          Event ID
        </span>

        <span class="meta-value">
          #{{ event.event_id }}
        </span>

      </div>

    </div>

  </div>

</template>

<style scoped>
.event-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.event-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.event-title {
  font-size: 20px;
  font-weight: 700;
}

.event-date {
  margin-top: 6px;
  color: var(--text-muted);
  font-size: 14px;
}

.event-card-footer {
  padding-top: 14px;
  border-top: 1px solid var(--border-color);
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-label {
  font-size: 12px;
  color: var(--text-muted);
}

.meta-value {
  font-weight: 600;
}
</style>