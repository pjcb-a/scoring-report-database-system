<script setup>
import { reactive } from 'vue'

import Input from '@/components/ui/Input.vue'
import PrimaryButton from '@/components/ui/PrimaryButton.vue'

const emit = defineEmits([
  'submit'
])

const form = reactive({

  team_name: '',

  team_color: ''
})

const submitForm = () => {

  emit('submit', {
    ...form
  })

  form.team_name = ''

  form.team_color = ''
}
</script>

<template>

  <form
    class="team-form"
    @submit.prevent="submitForm"
  >

    <Input
      v-model="form.team_name"
      label="Team Name"
      placeholder="Enter team name"
    />

    <Input
      v-model="form.team_color"
      label="Team Color"
      placeholder="Enter team color"
    />

    <div class="form-actions">

      <PrimaryButton>
        Save Team
      </PrimaryButton>

    </div>

  </form>

</template>

<style scoped>
.team-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}
</style>