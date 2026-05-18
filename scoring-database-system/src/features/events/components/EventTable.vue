<script setup>
import Badge from '@/components/ui/Badge.vue'

    defineProps({
    events: {
        type: Array,
        required: true
    }
    })
</script>

<template>
  <div class="card-base">

    <table class="data-table">

      <thead>
        <tr>
          <th>Event Name</th>
          <th>Start Date</th>
          <th>End Date</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="event in events"
          :key="event.event_id"
        >

          <td>
            {{ event.event_name }}
          </td>

          <td>
            {{ event.start_day }}
          </td>

          <td>
            {{ event.end_day }}
          </td>

          <td>

            <Badge
              :variant="
                event.status === 'Active'
                  ? 'success'
                  : 'primary'
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
