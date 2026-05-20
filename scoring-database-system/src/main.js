import { createApp } from 'vue'

import { createPinia } from 'pinia'

import App from './App.vue'

import router from './router'

import './assets/css/index.css'

import { useEventContextStore }
from '@/features/events/store/eventContextStore'


const app = createApp(App)

const pinia = createPinia()


app.use(pinia)

app.use(router)


/*
--------------------------------------------------
LOAD GLOBAL EVENT CONTEXT
--------------------------------------------------
*/

const eventContextStore =
  useEventContextStore()

eventContextStore.loadStoredEvent()


app.mount('#app')