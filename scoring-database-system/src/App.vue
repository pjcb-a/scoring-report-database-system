<script setup>
  import DashboardLayout from './layouts/DashBoardLayout.vue'
  import Toast from '@/components/ui/Toast.vue'
  import { useToastStore } from '@/features/events/store/toastStore'
  import { storeToRefs } from 'pinia'


const toastStore =
  useToastStore()

const {

  toasts

} = storeToRefs(
  toastStore
)
</script>
    
<template>
  <DashboardLayout>
    <router-view />
  </DashboardLayout>

  <div class="toast-container">

  <Toast

    v-for="toast in toasts"

    :key="toast.id"

    :message="toast.message"

    :type="toast.type"
  />

</div>
</template>

<style scoped>
.toast-container {

  position: fixed;

  top: 20px;

  right: 20px;

  display: flex;

  flex-direction: column;

  gap: 12px;

  z-index: 9999;
}
</style>
