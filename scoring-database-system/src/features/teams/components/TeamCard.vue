<script setup>

const props = defineProps({

  team: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['delete'])

const deleteTeam = () => {

  const confirmed = window.confirm(

    `Delete "${props.team.team_name}"?`
  )

  if (!confirmed) {
    return
  }

  emit(
    'delete',
    props.team.team_id
  )
}

</script>

<template>

  <div class="team-card">

    <div class="team-card-header">

      <div>

        <h3>
          {{ team.team_name }}
        </h3>

        <p class="team-color-label">
          {{ team.team_color }}
        </p>

      </div>

      <div class="team-card-actions">

        <span
          class="team-color-preview"
          :style="{
            backgroundColor:
              team.team_color
          }"
        />

        <button
          type="button"
          class="delete-team-btn"
          aria-label="Delete team"
          @click="deleteTeam"
        >
          <i class="fa-solid fa-trash"></i>
        </button>

      </div>

    </div>

  </div>

</template>

<style scoped>

.team-card {

  background-color: white;

  border:
    1px solid var(--border-color);

  border-radius: var(--radius-lg);

  padding: 1.25rem;

  transition: 0.2s ease;
}

.team-card:hover {

  box-shadow:
    0 4px 16px rgba(0, 0, 0, 0.08);

  transform: translateY(-1px);
}

.team-card-header {

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 0.75rem;
}

.team-card-header h3 {

  font-size: 1.05rem;

  font-weight: 700;

  margin: 0;
}

.team-color-label {

  margin-top: 0.35rem;

  font-size: 0.85rem;

  color: var(--text-muted);
}

.team-card-actions {

  display: flex;

  align-items: center;

  gap: 0.75rem;

  flex-shrink: 0;
}

.team-color-preview {

  width: 36px;

  height: 36px;

  border-radius: 50%;

  border:
    2px solid var(--border-color);
}

.delete-team-btn {

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 0.5rem;

  padding: 0.8rem;

  border: none;

  border-radius: 10px;

  color: white;

  cursor: pointer;

  transition: 0.2s ease;

  background: #dc2626;
}

.delete-team-btn:hover {

  background: #b91c1c;
}

</style>
