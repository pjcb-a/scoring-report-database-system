<script setup>
import { reactive } from 'vue'
    
import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'
    
    const emit = defineEmits(['submit'])
    
    const form = reactive({
      event_name: '',
      start_day: '',
      end_day: ''
    })
    
    const submitForm = () => {
    
      emit('submit', {
        ...form,
        status: 'Active'
      })
    
      form.event_name = ''
      form.start_day = ''
      form.end_day = ''
    }
</script>

<template>

  <form
    class="event-form"
    @submit.prevent="submitForm"
  >

    <Input
      v-model="form.event_name"
      label="Event Name"
      placeholder="Enter event name"
    />

    <Input
      v-model="form.start_day"
      type="date"
      label="Start Date"
    />

    <Input
      v-model="form.end_day"
      type="date"
      label="End Date"
    />

    <div class="form-actions">

      <PrimaryButton>
        Save Event
      </PrimaryButton>

    </div>

  </form>

</template>


<style scoped>
.event-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>