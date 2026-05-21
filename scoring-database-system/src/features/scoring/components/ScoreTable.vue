<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  scores: {
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

          <th>Winner</th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="score in scores"
          :key="score.game_score_id"
        >

          <td>
            {{ score.team }}
          </td>

          <td>
            {{ score.total_score }}
          </td>

          <td>
            {{ score.rank_position || '-' }}
          </td>

          <td>

            <Badge
              :variant="
                score.is_winner
                  ? 'success'
                  : 'primary'
              "
            >
              {{
                score.is_winner
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