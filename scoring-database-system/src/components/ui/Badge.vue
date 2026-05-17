<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary'
  }
})

const badgeClass = computed(() => {
  return `badge badge-${props.variant}`
})
</script>

<template>

  <span :class="badgeClass">
    <slot />
  </span>

</template>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;

  padding: 6px 12px;

  border-radius: 999px;

  font-size: 12px;
  font-weight: 700;
}

.badge-primary {
  background-color: var(--adnu-blue-light);
  color: var(--adnu-blue-dark);
}

.badge-success {
  background-color: #DCFCE7;
  color: #166534;
}

.badge-danger {
  background-color: var(--adnu-danger-light);
  color: var(--adnu-danger);
}
</style>