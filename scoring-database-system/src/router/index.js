import { createRouter, createWebHistory } from 'vue-router'

import DashboardPage from '@/features/dashboard/pages/DashboardPage.vue'
import EventPage from '@/features/events/pages/EventPage.vue'
import SportPage from '@/features/sports/pages/SportPage.vue'
import TeamPage from '@/features/teams/pages/TeamPage.vue'
import GamePage from '@/features/games/pages/GamePage.vue'
import ReportsPage from '@/features/reports/pages/ReportsPage.vue'

const routes = [
  {
    path: '/',
    component: DashboardPage
  },
  {
    path: '/events',
    component: EventPage
  },
  {
    path: '/sports',
    component: SportPage
  },
  {
    path: '/teams',
    component: TeamPage
  },
  {
    path: '/games',
    component: GamePage
  },
  {
    path: '/reports',
    component: ReportsPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router