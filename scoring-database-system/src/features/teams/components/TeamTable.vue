<script setup>
defineProps({

  teams: {
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
            Team Name
          </th>

          <th>
            Team Color
          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="team in teams"
          :key="team.team_id"
        >

          <td>
            {{ team.team_name }}
          </td>

          <td>

            <div class="team-color">

              <span
                class="color-preview"
                :style="{
                  backgroundColor:
                    team.team_color
                }"
              />

              {{ team.team_color }}

            </div>

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

.team-color {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-preview {
  width: 18px;
  height: 18px;

  border-radius: 50%;

  border:
    1px solid var(--border-color);
}
</style>