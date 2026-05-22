<script setup>

import { onMounted, ref } from 'vue'

import { useRouter } from 'vue-router'

import { storeToRefs } from 'pinia'

import {

  useEventContextStore

} from '@/features/events/store/eventContextStore'

import {

  useTeamStore

} from '../store/teamStore'

import TeamForm from '../components/TeamForm.vue'

import TeamCard from '../components/TeamCard.vue'


/*
|--------------------------------------------------------------------------
| ROUTER
|--------------------------------------------------------------------------
*/

const router = useRouter()

/*
|--------------------------------------------------------------------------
| EVENT CONTEXT
|--------------------------------------------------------------------------
*/

const eventContextStore =
  useEventContextStore()

const {

  currentEvent

} = storeToRefs(
  eventContextStore
)

/*
|--------------------------------------------------------------------------
| TEAM STORE
|--------------------------------------------------------------------------
*/

const teamStore =
  useTeamStore()

const {

  teams,

  loading,

  error

} = storeToRefs(
  teamStore
)


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const showTeamForm = ref(false)


/*
|--------------------------------------------------------------------------
| INITIALIZE
|--------------------------------------------------------------------------
*/

onMounted(async () => {

  if (!currentEvent.value) {

    router.push('/events')

    return
  }

  await teamStore.loadTeams()
})

/*
|--------------------------------------------------------------------------
| DELETE TEAM
|--------------------------------------------------------------------------
*/

const handleDeleteTeam =
  async (teamId) => {

    try {

      await teamStore.removeTeam(teamId)

    } catch (err) {

      console.error(err)
    }
  }

</script>

<template>

  <section class="team-page">

    <div class="team-page-header">

      <div>
        <h1>
          Teams
        </h1>

        <p>
          Manage event teams.
        </p>
      </div>

      <button
        class="add-team-btn"
        @click="showTeamForm = true"
      >
        <i class="fa-solid fa-plus"></i>

        Add Team
      </button>

    </div>

    <TeamForm
      v-if="showTeamForm"
      @close="showTeamForm = false"
      @success="showTeamForm = false"
    />

    <div
      v-if="loading"
      class="loading-state"
    >
      Loading teams...
    </div>

    <div
      v-else-if="error"
      class="team-error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="!teams.length"
      class="empty-state"
    >
      No teams found. Add your first team.
    </div>

    <div
      v-else
      class="team-grid"
    >

      <TeamCard
        v-for="team in teams"
        :key="team.team_id"
        :team="team"
        @delete="handleDeleteTeam"
      />

    </div>

  </section>

</template>

<style scoped>

.team-page {

  display: flex;

  flex-direction: column;

  gap: 1.5rem;
}

.team-page-header {

  display: flex;

  align-items: center;

  justify-content: space-between;
}

.team-page-header h1 {

  font-size: 32px;

  font-weight: 800;
}

.team-page-header p {

  margin-top: 6px;

  color: var(--text-muted);
}

.add-team-btn {

  display: flex;

  align-items: center;

  gap: 0.6rem;

  padding: 0.8rem 1rem;

  border: none;

  border-radius: 10px;

  background: #2563eb;

  color: white;

  cursor: pointer;

  font-weight: 600;

  transition: 0.2s ease;
}

.add-team-btn:hover {

  background: #1d4ed8;
}

.loading-state,
.empty-state {

  padding: 2rem;

  border-radius: 12px;

  background: white;

  text-align: center;

  color: var(--text-muted);
}

.team-error {

  padding: 2rem;

  border-radius: 12px;

  background: white;

  text-align: center;

  color: var(--adnu-danger);
}

.team-grid {

  display: grid;

  grid-template-columns:
    repeat(auto-fill, minmax(260px, 1fr));

  gap: 1.25rem;
}

</style>
