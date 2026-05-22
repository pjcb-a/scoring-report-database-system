<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useReportStore } from '../store/reportsStore'

const reportStore = useReportStore()
const { sortBy, sortDirection, searchQuery, matches, displayedMatches } =
  storeToRefs(reportStore)

const directionOptions = computed(() => {
  if (sortBy.value === 'date') {
    return [
      { value: 'desc', label: 'Newest first' },
      { value: 'asc', label: 'Oldest first' }
    ]
  }

  return [
    { value: 'asc', label: 'A → Z' },
    { value: 'desc', label: 'Z → A' }
  ]
})
</script>

<template>
  <div class="reports-sort">
    <div class="reports-sort__controls">
      <div class="sort-field sort-field--search">
        <label for="report-search">Search</label>
        <input
          id="report-search"
          v-model="searchQuery"
          type="search"
          class="sort-select sort-search"
          placeholder="Sport, team, round, venue..."
        >
      </div>

      <div class="sort-field">
        <label for="sort-by">Sort by</label>
        <select
          id="sort-by"
          v-model="sortBy"
          class="sort-select"
        >
          <option value="date">
            Date
          </option>
          <option value="sport">
            Sport
          </option>
          <option value="team">
            Team
          </option>
        </select>
      </div>

      <div class="sort-field">
        <label for="sort-direction">Order</label>
        <select
          id="sort-direction"
          v-model="sortDirection"
          class="sort-select"
        >
          <option
            v-for="option in directionOptions"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>
    </div>

    <p class="reports-count">
      Showing {{ displayedMatches.length }} of {{ matches.length }} concluded match(es)
    </p>
  </div>
</template>

<style scoped>
.reports-sort {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  padding: 16px 18px;
  background: white;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 12px;
}

.reports-sort__controls {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.sort-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sort-field label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-muted, #64748b);
}

.sort-select {
  min-width: 150px;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  background: white;
}

.sort-field--search {
  flex: 1;
  min-width: 200px;
}

.sort-search {
  width: 100%;
  min-width: 220px;
}

.reports-count {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-muted, #64748b);
  font-weight: 600;
}
</style>
