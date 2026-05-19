<script setup>
defineProps({

  judgeScores: {
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

          <th>
            Team
          </th>

          <th>
            Criteria
          </th>

          <th>
            Judge
          </th>

          <th>
            Score
          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="score in judgeScores"
          :key="score.score_component_id"
        >

          <td>
            {{ score.team }}
          </td>

          <td>
            {{ score.criteria }}
          </td>

          <td>
            {{ score.judge }}
          </td>

          <td>
            {{ score.score_value }}
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