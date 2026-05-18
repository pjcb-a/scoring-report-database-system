import { computed, ref } from 'vue'

import {

  fetchReports,

  fetchEvents

} from '../services/reportsService'


const reports = ref([])

const events = ref([])

const loading = ref(false)

const error = ref(null)


const totalReports = computed(() => {
  return reports.value.length
})

const winners = computed(() => {

  return reports.value.filter(
    report => report.isWinner
  ).length
})


const loadReports = async () => {

  loading.value = true

  try {

    reports.value =
      await fetchReports()

  } catch (err) {

    console.error(err)

    error.value =
      'Failed to load reports.'

  } finally {

    loading.value = false
  }
}


const loadEvents = async () => {

  try {

    events.value =
      await fetchEvents()

  } catch (err) {

    console.error(err)
  }
}


export function useReportsStore() {

  return {

    reports,

    events,

    loading,

    error,

    totalReports,

    winners,

    loadReports,

    loadEvents
  }
}