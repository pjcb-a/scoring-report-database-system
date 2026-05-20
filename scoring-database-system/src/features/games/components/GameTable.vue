<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  games: {
    type: Array,
    required: true
  }
})

const formatDate = (date) => {

  if (!date) return 'N/A'

  return new Date(date)
    .toLocaleString()
}

const getBadgeVariant = (status) => {

  switch (status) {

    case 'Completed':
      return 'primary'

    case 'Ongoing':
      return 'success'

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
            Event Sport
          </th>

          <th>
            Round
          </th>

          <th>
            Start Date
          </th>

          <th>
            Venue
          </th>

          <th>
            Status
          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="game in games"
          :key="game.game_id"
        >

          <td>

            {{ game.event }}

            -

            {{ game.sport }}

          </td>

          <td>
            {{ game.round }}
          </td>

          <td>
            {{ formatDate(game.start_date) }}
          </td>

          <td>
            {{ game.venue_name || '-' }}
          </td>

          <td>

            <Badge
              :variant="
                getBadgeVariant(game.game_status)
              "
            >
              {{ game.game_status }}
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
</style>
