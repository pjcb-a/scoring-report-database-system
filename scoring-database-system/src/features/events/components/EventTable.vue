<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  events: {
    type: Array,
    required: true
  }
})

const formatDate = (date) => {

  if (!date) return 'N/A'

  return new Date(date)
    .toLocaleDateString()
}

const getBadgeVariant = (status) => {

  switch (status) {

    case 'Active':
      return 'success'

    case 'Completed':
      return 'primary'

    default:
      return 'warning'
  }
}
</script>

<template>

  <div class="card-base table-container">

    <table class="data-table">

      <thead>

        <tr>

          <th>
            Event Name
          </th>

          <th>
            Start Date
          </th>

          <th>
            End Date
          </th>

          <th>
            Status
          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="event in events"
          :key="event.event_id"
        >

          <td>

            <div class="event-name-cell">

              <span class="event-name">
                {{ event.event_name }}
              </span>

              <span class="event-id">
                #{{ event.event_id }}
              </span>

            </div>

          </td>

          <td>
            {{ formatDate(event.start_day) }}
          </td>

          <td>
            {{ formatDate(event.end_day) }}
          </td>

          <td>

            <Badge
              :variant="
                getBadgeVariant(event.status)
              "
            >
              {{ event.status }}
            </Badge>

          </td>

        </tr>

      </tbody>

    </table>

  </div>

</template>

<style scoped>
.table-container {
  overflow-x: auto;
}

.event-name-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.event-name {
  font-weight: 600;
}

.event-id {
  font-size: 12px;
  color: var(--text-muted);
}
</style>