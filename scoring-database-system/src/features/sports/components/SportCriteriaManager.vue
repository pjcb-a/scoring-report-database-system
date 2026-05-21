<script setup>
import { onMounted, ref } from 'vue'
import SportCriteriaEditor from './SportCriteriaEditor.vue'
import {
  getCriteriaByEventSport,
  createCriteria,
  deleteCriteria
} from '../services/criteriaService'

const props = defineProps({
  eventSportId: {
    type: Number,
    required: true
  }
})

const criteria = ref([])
const draftCriteria = ref([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')

const loadCriteria = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await getCriteriaByEventSport(props.eventSportId)
    criteria.value = response.data || []
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load criteria.'
  } finally {
    loading.value = false
  }
}

const saveDraftCriteria = async () => {
  if (!draftCriteria.value.length) {
    return
  }

  const draftTotal = draftCriteria.value.reduce(
    (sum, item) => sum + Number(item.percentage || 0),
    0
  )

  const existingTotal = criteria.value.reduce(
    (sum, item) => sum + Number(item.percentage || 0),
    0
  )

  if (existingTotal + draftTotal > 100) {
    error.value = 'Total criteria percentage cannot exceed 100%.'
    return
  }

  saving.value = true
  error.value = ''

  try {
    for (const item of draftCriteria.value) {
      await createCriteria(props.eventSportId, item)
    }

    draftCriteria.value = []
    await loadCriteria()
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Failed to save criteria.'
  } finally {
    saving.value = false
  }
}

const removeSavedCriteria = async (criteriaId) => {
  try {
    await deleteCriteria(criteriaId)
    criteria.value = criteria.value.filter(
      item => item.criteria_id !== criteriaId
    )
  } catch (err) {
    console.error(err)
    error.value = 'Failed to delete criteria.'
  }
}

onMounted(loadCriteria)
</script>

<template>
  <div class="criteria-manager">
    <p
      v-if="loading"
      class="criteria-manager__hint"
    >
      Loading criteria...
    </p>

    <ul
      v-else-if="criteria.length"
      class="saved-criteria"
    >
      <li
        v-for="item in criteria"
        :key="item.criteria_id"
      >
        <span>{{ item.criteria_name }}</span>
        <span>{{ item.percentage }}%</span>
        <button
          type="button"
          class="remove-btn"
          @click="removeSavedCriteria(item.criteria_id)"
        >
          Remove
        </button>
      </li>
    </ul>

    <p
      v-else
      class="criteria-manager__hint"
    >
      No criteria yet.
    </p>

    <SportCriteriaEditor v-model="draftCriteria" />

    <p
      v-if="error"
      class="criteria-manager__error"
    >
      {{ error }}
    </p>

    <button
      type="button"
      class="save-btn"
      :disabled="saving || !draftCriteria.length"
      @click="saveDraftCriteria"
    >
      {{ saving ? 'Saving...' : 'Save criteria' }}
    </button>
  </div>
</template>

<style scoped>
.criteria-manager {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.criteria-manager__hint {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
}

.criteria-manager__error {
  margin: 0;
  color: #b91c1c;
  font-size: 0.85rem;
  font-weight: 600;
}

.saved-criteria {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.saved-criteria li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
}

.saved-criteria li span:first-child {
  font-weight: 600;
}

.remove-btn,
.save-btn {
  border: none;
  border-radius: 8px;
  padding: 6px 10px;
  font-weight: 600;
  cursor: pointer;
}

.remove-btn {
  margin-left: auto;
  background: #fee2e2;
  color: #b91c1c;
}

.save-btn {
  align-self: flex-start;
  background: #2563eb;
  color: white;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
