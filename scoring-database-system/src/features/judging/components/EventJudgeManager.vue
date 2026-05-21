<script setup>
import { onMounted, ref, nextTick } from 'vue'
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
import {
  getJudgesByEvent,
  createJudge,
  deleteJudge
} from '../services/judgingService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { storeToRefs } from 'pinia'

const eventContextStore = useEventContextStore()
const { currentEventId } = storeToRefs(eventContextStore)

const judges = ref([])
const judgeName = ref('')
const loading = ref(false)
const saving = ref(false)
const error = ref('')

const loadJudges = async () => {
  if (!currentEventId.value) {
    return
  }

  loading.value = true
  error.value = ''

  try {
    const response = await getJudgesByEvent(currentEventId.value)
    judges.value = response.data || []
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load judges.'
  } finally {
    loading.value = false
  }
}

const addJudge = async () => {
  const name = judgeName.value.trim()

  if (!name) {
    error.value = 'Judge name is required.'
    return
  }

  if (!currentEventId.value) {
    return
  }

  saving.value = true
  error.value = ''

  try {
    await createJudge(currentEventId.value, { judge_name: name })
    judgeName.value = ''
    await loadJudges()
  } catch (err) {
    console.error(err)
    error.value = err.message || 'Failed to add judge.'
  } finally {
    saving.value = false
  }
}

const removeJudge = async (judgeId) => {
  try {
    await deleteJudge(judgeId)
    judges.value = judges.value.filter(
      judge => judge.judge_id !== judgeId
    )
  } catch (err) {
    console.error(err)
    error.value = 'Failed to remove judge.'
  }
}

onMounted(async () => {
  // Delay loading to avoid router cancellation
  await nextTick()
  setTimeout(() => {
    loadJudges()
  }, 100)
})

defineExpose({ loadJudges, judges })
</script>

<template>
  <div class="judge-manager">
    <div class="judge-manager__header">
      <h4>Judges</h4>
      <p>
        Add judges for this event. Each judge scores every criteria for each team when finalizing component-score matches.
      </p>
    </div>

    <p
      v-if="loading"
      class="judge-manager__hint"
    >
      Loading judges...
    </p>

    <ul
      v-else-if="judges.length"
      class="judge-list"
    >
      <li
        v-for="judge in judges"
        :key="judge.judge_id"
      >
        <span>{{ judge.judge_name }}</span>
        <button
          type="button"
          class="remove-btn"
          @click="removeJudge(judge.judge_id)"
        >
          Remove
        </button>
      </li>
    </ul>

    <p
      v-else
      class="judge-manager__hint"
    >
      No judges yet.
    </p>

    <div class="judge-add">
      <Input
        v-model="judgeName"
        label="Judge name"
        placeholder="Enter judge name"
      />
      <p
        v-if="error"
        class="judge-manager__error"
      >
        {{ error }}
      </p>
      <PrimaryButton
        type="button"
        :disabled="saving"
        @click="addJudge"
      >
        {{ saving ? 'Adding...' : 'Add judge' }}
      </PrimaryButton>
    </div>
  </div>
</template>

<style scoped>
.judge-manager {
  padding: 14px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.judge-manager__header h4 {
  margin: 0 0 4px;
}

.judge-manager__header p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
}

.judge-manager__hint {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-muted, #64748b);
}

.judge-manager__error {
  margin: 0;
  color: #b91c1c;
  font-size: 0.85rem;
  font-weight: 600;
}

.judge-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.judge-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-weight: 600;
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

.judge-add {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
