import { createRouter, createWebHistory } from 'vue-router'

import DashboardPage from '@/features/dashboard/pages/DashboardPage.vue'
import EventPage from '@/features/events/pages/EventPage.vue'
import SportPage from '@/features/sports/pages/SportPage.vue'
import TeamPage from '@/features/teams/pages/TeamPage.vue'
import GamePage from '@/features/games/pages/GamePage.vue'
import ScoringPage from '@/features/scoring/pages/ScoringPage.vue'
import JudgePage from '@/features/judging/pages/JudgePage.vue'
import ReportsPage from '@/features/reports/pages/ReportsPage.vue'

import { useEventContextStore }
  from '@/features/events/store/eventContextStore'
import { cancelAllPendingRequests } from '@/services/api'

const routes = [

  {
    path: '/',

    redirect: '/events'
  },

  {
    path: '/events',

    name: 'events',

    component: EventPage
  },

  {
    path: '/events/:eventId/dashboard',

    name: 'event-dashboard',

    component: DashboardPage,

    meta: {
      requiresEvent: true
    }
  },

  {
    path: '/events/:eventId/sports',

    name: 'event-sports',

    component: SportPage,

    meta: {
      requiresEvent: true
    }
  },

  {
    path: '/events/:eventId/teams',

    name: 'event-teams',

    component: TeamPage,

    meta: {
      requiresEvent: true
    }
  },

  {
    path: '/events/:eventId/games',

    name: 'event-games',

    component: GamePage,

    meta: {
      requiresEvent: true
    }
  },

  {
    path: '/events/:eventId/scoring',

    name: 'event-scoring',

    component: ScoringPage,

    meta: {
      requiresEvent: true
    }
  },

  {
    path: '/events/:eventId/judging',

    name: 'event-judging',

    component: JudgePage,

    meta: {
      requiresEvent: true
    }
  },

  {
    path: '/events/:eventId/reports',

    name: 'event-reports',

    component: ReportsPage,

    meta: {
      requiresEvent: true
    }
  }
]

/*
|--------------------------------------------------------------------------
| ROUTER INSTANCE
|--------------------------------------------------------------------------
*/

const router = createRouter({

  history: createWebHistory(),

  routes
})

/*
|--------------------------------------------------------------------------
| GLOBAL ROUTE GUARD
|--------------------------------------------------------------------------
*/

router.beforeEach((to, from, next) => {
  // Cancel all pending network requests from the previous page/tab
  cancelAllPendingRequests('Navigated to ' + to.path)

  const eventContextStore =
    useEventContextStore()

  /*
  --------------------------------------------------------------------------
  CHECK IF ROUTE REQUIRES EVENT CONTEXT
  --------------------------------------------------------------------------
  */

  if (

    to.meta.requiresEvent

    &&

    !eventContextStore.hasSelectedEvent

  ) {

    return next('/events')
  }

  next()
})

/*
|--------------------------------------------------------------------------
| EXPORT ROUTER
|--------------------------------------------------------------------------
*/

export default router