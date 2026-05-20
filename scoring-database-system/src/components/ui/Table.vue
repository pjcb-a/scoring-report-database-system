<script setup>

defineProps({

  columns: {
    type: Array,
    default: () => []
  },

  rows: {
    type: Array,
    default: () => []
  }
})

</script>

<template>

  <div class="table-wrapper">

    <table class="table">

      <thead>

        <tr>

          <th
            v-for="column in columns"
            :key="column.key"
          >

            {{ column.label }}

          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="(
            row,
            index
          ) in rows"

          :key="index"
        >

          <td
            v-for="column in columns"
            :key="column.key"
          >

            {{ row[column.key] }}

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

  border-radius:
    var(--radius-lg);

  border:
    1px solid var(--border-color);

  background-color:
    var(--white);

  box-shadow:
    var(--shadow-sm);
}

.table {

  width: 100%;

  border-collapse: collapse;
}

.table thead {

  background-color:
    var(--adnu-blue-dark);

  color:
    var(--white);
}

.table th,
.table td {

  padding: 16px;

  text-align: left;

  border-bottom:
    1px solid var(--border-color);
}

.table tbody tr {

  transition:
    var(--transition-fast);
}

.table tbody tr:hover {

  background-color:
    var(--bg-gray-light);
}

</style>