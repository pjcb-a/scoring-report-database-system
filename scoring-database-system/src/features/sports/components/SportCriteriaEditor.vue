<script setup>
import { computed, ref } from 'vue'
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const draftName = ref('')
const draftPercentage = ref('')
const localError = ref('')

const criteria = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const totalPercentage = computed(() =>
  criteria.value.reduce(
    (sum, item) => sum + Number(item.percentage || 0),
    0
  )
)

const remainingPercentage = computed(() =>
  Math.max(0, 100 - totalPercentage.value)
)

const addCriteria = () => {
  localError.value = ''

  const name = draftName.value.trim()
  const percentage = Number(draftPercentage.value)

  if (!name) {
    localError.value = 'Criteria name is required.'
    return
  }

  if (Number.isNaN(percentage) || percentage <= 0) {
    localError.value = 'Enter a valid percentage greater than 0.'
    return
  }

  if (totalPercentage.value + percentage > 100) {
    localError.value = `Total cannot exceed 100%. Only ${remainingPercentage.value}% remaining.`
    return
  }

  criteria.value = [
    ...criteria.value,
    {
      criteria_name: name,
      percentage
    }
  ]

  draftName.value = ''
  draftPercentage.value = ''
}

const removeCriteria = (index) => {
  criteria.value = criteria.value.filter((_, i) => i !== index)
}
</script>

<template>
  <div class="criteria-editor">
    <div class="criteria-editor__header">
      <h4>Scoring criteria</h4>
      <p>
        Add criteria for this component-based sport. Total must not exceed 100%.
      </p>
      <div
        class="criteria-total"
        :class="{
          'criteria-total--complete': totalPercentage === 100,
          'criteria-total--over': totalPercentage > 100
        }"
      >
        Total: {{ totalPercentage }}% / 100%
      </div>
    </div>

    <ul
      v-if="criteria.length"
      class="criteria-list"
    >
      <li
        v-for="(item, index) in criteria"
        :key="`${item.criteria_id || item.criteria_name}-${index}`"
        class="criteria-item"
      >
        <div>
          <strong>{{ item.criteria_name }}</strong>
          <span>{{ item.percentage }}%</span>
        </div>
        <button
          v-if="!readonly"
          type="button"
          class="remove-btn"
          @click="removeCriteria(index)"
        >
          Remove
        </button>
      </li>
    </ul>

    <div
      v-if="!readonly"
      class="criteria-add"
    >
      <Input
        v-model="draftName"
        label="Criteria name"
        placeholder="e.g. Technique"
      />
      <Input
        v-model="draftPercentage"
        label="Percentage"
        type="number"
        min="0"
        :max="remainingPercentage"
        placeholder="%"
      />
      <p
        v-if="localError"
        class="criteria-error"
      >
        {{ localError }}
      </p>
      <PrimaryButton
        type="button"
        @click="addCriteria"
      >
        Add criteria
      </PrimaryButton>
    </div>
  </div>
</template>

<style scoped>
.criteria-editor {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 14px;
  border-radius: 12px;
  border: 1px solid #dbeafe;
  background: #f8fbff;
}

.criteria-editor__header h4 {
  margin: 0 0 4px;
}

.criteria-editor__header p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
}

.criteria-total {
  margin-top: 10px;
  font-weight: 700;
  font-size: 0.9rem;
}

.criteria-total--complete {
  color: #166534;
}

.criteria-total--over {
  color: #b91c1c;
}

.criteria-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.criteria-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  background: white;
  border: 1px solid #e2e8f0;
}

.criteria-item div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.criteria-item span {
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
}

.remove-btn {
  border: none;
  background: #fee2e2;
  color: #b91c1c;
  padding: 6px 10px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.criteria-add {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.criteria-error {
  margin: 0;
  color: #b91c1c;
  font-size: 0.85rem;
  font-weight: 600;
}
</style>
