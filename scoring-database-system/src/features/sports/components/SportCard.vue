<script setup>
import Badge from '@/components/ui/Badge.vue'

const props = defineProps({

  sport: {
    type: Object,
    required: true
  }
})

const emit = defineEmits([
  'delete'
])

/*
|--------------------------------------------------------------------------
| DELETE SPORT
|--------------------------------------------------------------------------
*/

const removeSport = () => {

  emit(
    'delete',
    props.sport.event_sport_id
  )
}
</script>

<template>

  <div class="sport-card card-base">

    <div class="sport-top">

      <div>

        <h2>
          {{ sport.sport_name }}
        </h2>

        <p class="sport-description">
          Event Sport
        </p>

      </div>

      <Badge variant="primary">
        {{ sport.scoring_type }}
      </Badge>

    </div>

    <div class="sport-actions">

      <button
        class="delete-btn"
        @click="removeSport"
      >
        <i class="fa-solid fa-trash"></i>

        Remove
      </button>

    </div>

  </div>

</template>

<style scoped>
.sport-card {

  display: flex;

  flex-direction: column;

  gap: 1rem;
}

.sport-top {

  display: flex;

  justify-content: space-between;

  align-items: flex-start;

  gap: 1rem;
}

.sport-description {

  margin-top: 0.35rem;

  color: #6b7280;

  font-size: 0.9rem;
}

.sport-actions {

  display: flex;

  justify-content: flex-end;
}

.delete-btn {

  display: flex;

  align-items: center;

  gap: 0.5rem;

  padding: 0.7rem 1rem;

  border: none;

  border-radius: 10px;

  background: #dc2626;

  color: white;

  cursor: pointer;

  transition: 0.2s ease;
}

.delete-btn:hover {

  background: #b91c1c;
}
</style>