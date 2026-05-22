<script setup>
import { storeToRefs } from 'pinia'
import { useReportStore } from '../store/reportsStore'

const reportStore = useReportStore()

const {
  sportOptions,
  teamOptions,
  dayOptions,
  selectedSports,
  selectedTeams,
  selectedDays
} = storeToRefs(reportStore)

const {
  toggleSport,
  toggleTeam,
  toggleDay,
  selectAllSports,
  clearSports,
  selectAllTeams,
  clearTeams,
  selectAllDays,
  clearDays
} = reportStore
</script>

<template>
  <aside class="reports-filters">
    <h3>Filter by</h3>

    <section class="filter-group">
      <div class="filter-group__header">
        <h4>Sport</h4>
        <div class="filter-actions">
          <button
            type="button"
            @click="selectAllSports"
          >
            All
          </button>
          <button
            type="button"
            @click="clearSports"
          >
            None
          </button>
        </div>
      </div>

      <div
        v-if="!sportOptions.length"
        class="filter-empty"
      >
        No sports in reports yet.
      </div>

      <label
        v-for="sport in sportOptions"
        :key="sport"
        class="filter-option"
      >
        <input
          type="checkbox"
          :checked="selectedSports.includes(sport)"
          @change="toggleSport(sport)"
        >
        <span>{{ sport }}</span>
      </label>
    </section>

    <section class="filter-group">
      <div class="filter-group__header">
        <h4>Team</h4>
        <div class="filter-actions">
          <button
            type="button"
            @click="selectAllTeams"
          >
            All
          </button>
          <button
            type="button"
            @click="clearTeams"
          >
            None
          </button>
        </div>
      </div>

      <div
        v-if="!teamOptions.length"
        class="filter-empty"
      >
        No teams in reports yet.
      </div>

      <label
        v-for="team in teamOptions"
        :key="team"
        class="filter-option"
      >
        <input
          type="checkbox"
          :checked="selectedTeams.includes(team)"
          @change="toggleTeam(team)"
        >
        <span>{{ team }}</span>
      </label>
    </section>

    <section class="filter-group">
      <div class="filter-group__header">
        <h4>Day</h4>
        <div class="filter-actions">
          <button
            type="button"
            @click="selectAllDays"
          >
            All
          </button>
          <button
            type="button"
            @click="clearDays"
          >
            None
          </button>
        </div>
      </div>

      <div
        v-if="!dayOptions.length"
        class="filter-empty"
      >
        No dates in reports yet.
      </div>

      <label
        v-for="day in dayOptions"
        :key="day.key"
        class="filter-option"
      >
        <input
          type="checkbox"
          :checked="selectedDays.includes(day.key)"
          @change="toggleDay(day.key)"
        >
        <span>{{ day.label }}</span>
      </label>
    </section>
  </aside>
</template>

<style scoped>
.reports-filters {
  background: white;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 14px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  position: sticky;
  top: 16px;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
}

.reports-filters h3 {
  margin: 0;
  font-size: 1rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-group__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.filter-group__header h4 {
  margin: 0;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted, #64748b);
}

.filter-actions {
  display: flex;
  gap: 6px;
}

.filter-actions button {
  border: none;
  background: #f3f4f6;
  color: #374151;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
}

.filter-actions button:hover {
  background: #e5e7eb;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 4px 0;
}

.filter-empty {
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
  margin: 0;
}
</style>
