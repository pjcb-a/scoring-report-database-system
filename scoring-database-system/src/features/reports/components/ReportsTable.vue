<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  reports: {
    type: Array,
    required: true
  }
})
</script>

<template>

  <div class="card-base table-container">

    <table class="data-table">

      <thead>

        <tr>

          <th>Team</th>

          <th>Score</th>

          <th>Rank</th>

          <th>Status</th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="report in reports"
          :key="report.game_score_id"
        >

          <td>
            {{ report.team }}
          </td>

          <td>
            {{ report.score_value }}
          </td>

          <td>
            {{ report.rank_position || '-' }}
          </td>

          <td>

            <Badge
              :variant="
                report.isWinner
                  ? 'success'
                  : 'primary'
              "
            >
              {{
                report.isWinner
                  ? 'Winner'
                  : 'Participant'
              }}
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