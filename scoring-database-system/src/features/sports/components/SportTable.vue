<script setup>
import Badge from '@/components/ui/Badge.vue'

defineProps({

  sports: {
    type: Array,
    required: true
  },

  currentEventId: {
    type: Number,
    default: null
  }
})
</script>

<template>

  <div
    v-if="!currentEventId"
    class="empty-state"
  >
    Please select an event first.
  </div>

  <div
    v-else
    class="card-base table-container"
  >

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
          :key="sport.event_sport_id"
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

.empty-state {

  padding: 2rem;

  border-radius: 12px;

  background: white;

  text-align: center;

  color: #6b7280;
}
</style>