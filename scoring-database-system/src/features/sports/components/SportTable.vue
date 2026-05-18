<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  sports: {
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
            Sport
          </th>

          <th>
            Scoring Type
          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="sport in sports"
          :key="sport.sport_id"
        >

          <td>
            {{ sport.sport_name }}
          </td>

          <td>

            <Badge variant="primary">
              {{ sport.scoring_type }}
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