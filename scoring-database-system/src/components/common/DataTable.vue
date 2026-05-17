<script setup>
    defineProps({
      headers: {
        type: Array,
        required: true
      },
    
      rows: {
        type: Array,
        required: true
        }
    })
</script>

<template>
  <div class="table-wrapper">

    <table class="data-table">

      <thead>
        <tr>
          <th
            v-for="header in headers"
            :key="header"
          >
            {{ header }}
          </th>
        </tr>
      </thead>

      <tbody>

        <tr
          v-for="(row, index) in rows"
          :key="index"
        >

          <td
            v-for="(value, key) in row"
            :key="key"
          >
            {{ value }}
          </td>

        </tr>

        <tr v-if="rows.length === 0">
          <td
            :colspan="headers.length"
            class="empty-state"
          >
            No records found.
          </td>
        </tr>

      </tbody>

    </table>

  </div>
</template>


<style scoped>
.table-wrapper {
  width: 100%;
  overflow-x: auto;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: var(--text-muted);
}
</style>