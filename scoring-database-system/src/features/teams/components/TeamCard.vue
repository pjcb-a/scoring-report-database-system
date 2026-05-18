<script setup>
defineProps({

  team: {
    type: Object,
    required: true
  }
})
</script>

<template>

  <div class="team-card card-base">

    <div class="team-top">

      <div>

        <h2>
          {{ team.team_name }}
        </h2>

        <p>
          {{ team.team_color }}
        </p>

      </div>

      <span
        class="team-color-preview"
        :style="{
          backgroundColor:
            team.team_color
        }"
      />

    </div>

  </div>

</template>

<style scoped>
.team-card {
  display: flex;
  flex-direction: column;
}

.team-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.team-color-preview {
  width: 32px;
  height: 32px;

  border-radius: 50%;

  border:
    2px solid var(--border-color);
}
</style>