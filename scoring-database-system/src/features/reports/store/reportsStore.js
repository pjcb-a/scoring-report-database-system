import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getMatchReports } from '../services/reportsService'
import { useEventContextStore } from '@/features/events/store/eventContextStore'
import { runAsync } from '@/utils/request'
import {
  compareMatches,
  formatDayLabel,
  getDateKey,
  getSportName,
  getTeamNames
} from '../utils/matchReportUtils'
import { isFinalizedGame } from '@/utils/gameLifecycle'

export const useReportStore = defineStore('reportStore', () => {
  const matches = ref([])
  const loading = ref(false)
  const error = ref(null)

  const sortBy = ref('date')
  const sortDirection = ref('desc')

  const selectedSports = ref([])
  const selectedTeams = ref([])
  const selectedDays = ref([])
  const searchQuery = ref('')

  const eventContextStore = useEventContextStore()

  const sportOptions = computed(() => {
    const names = new Set(matches.value.map(getSportName))
    return [...names].sort((a, b) => a.localeCompare(b))
  })

  const teamOptions = computed(() => {
    const names = new Set()

    for (const match of matches.value) {
      for (const name of getTeamNames(match)) {
        names.add(name)
      }
    }

    return [...names].sort((a, b) => a.localeCompare(b))
  })

  const dayOptions = computed(() => {
    const keys = new Set(matches.value.map(getDateKey))

    return [...keys].sort((a, b) => {
      if (a === 'undated') {
        return 1
      }

      if (b === 'undated') {
        return -1
      }

      return a.localeCompare(b)
    }).map(key => ({
      key,
      label: formatDayLabel(key)
    }))
  })

  const syncFilterDefaults = () => {
    selectedSports.value = [...sportOptions.value]
    selectedTeams.value = [...teamOptions.value]
    selectedDays.value = dayOptions.value.map(day => day.key)
  }

  const matchesSearchText = (match) => {
    const query = searchQuery.value.trim().toLowerCase()

    if (!query) {
      return true
    }

    const parts = [
      match.game_name,
      match.sport,
      match.round,
      match.game_status,
      match.venue_name,
      match.scoring_type,
      ...(match.teams || []).map(team => team.team_name),
      ...(match.scores || []).map(score => score.team)
    ]

    return parts.some(
      part => part && String(part).toLowerCase().includes(query)
    )
  }

  const filteredMatches = computed(() =>
    matches.value.filter(match => {
      if (!matchesSearchText(match)) {
        return false
      }

      if (
        selectedSports.value.length
        && !selectedSports.value.includes(getSportName(match))
      ) {
        return false
      }

      const matchTeams = getTeamNames(match)

      if (
        selectedTeams.value.length
        && !matchTeams.some(team => selectedTeams.value.includes(team))
      ) {
        return false
      }

      if (
        selectedDays.value.length
        && !selectedDays.value.includes(getDateKey(match))
      ) {
        return false
      }

      return true
    })
  )

  const displayedMatches = computed(() => {
    const list = [...filteredMatches.value]

    list.sort((a, b) =>
      compareMatches(a, b, sortBy.value, sortDirection.value)
    )

    return list
  })

  const loadMatchReports = async () => {
    if (!eventContextStore.currentEventId) {
      return
    }

    await runAsync({ loading, error }, async () => {
      const response = await getMatchReports(
        eventContextStore.currentEventId
      )
      const allMatches = response?.data ?? []
      matches.value = allMatches.filter(isFinalizedGame)
      syncFilterDefaults()
    })
  }

  const toggleSport = (sport) => {
    if (selectedSports.value.includes(sport)) {
      selectedSports.value = selectedSports.value.filter(
        item => item !== sport
      )
    } else {
      selectedSports.value = [...selectedSports.value, sport]
    }
  }

  const toggleTeam = (team) => {
    if (selectedTeams.value.includes(team)) {
      selectedTeams.value = selectedTeams.value.filter(
        item => item !== team
      )
    } else {
      selectedTeams.value = [...selectedTeams.value, team]
    }
  }

  const toggleDay = (dayKey) => {
    if (selectedDays.value.includes(dayKey)) {
      selectedDays.value = selectedDays.value.filter(
        item => item !== dayKey
      )
    } else {
      selectedDays.value = [...selectedDays.value, dayKey]
    }
  }

  const selectAllSports = () => {
    selectedSports.value = [...sportOptions.value]
  }

  const clearSports = () => {
    selectedSports.value = []
  }

  const selectAllTeams = () => {
    selectedTeams.value = [...teamOptions.value]
  }

  const clearTeams = () => {
    selectedTeams.value = []
  }

  const selectAllDays = () => {
    selectedDays.value = dayOptions.value.map(day => day.key)
  }

  const clearDays = () => {
    selectedDays.value = []
  }

  return {
    matches,
    loading,
    error,
    sortBy,
    sortDirection,
    selectedSports,
    selectedTeams,
    selectedDays,
    searchQuery,
    sportOptions,
    teamOptions,
    dayOptions,
    displayedMatches,
    filteredMatches,
    loadMatchReports,
    toggleSport,
    toggleTeam,
    toggleDay,
    selectAllSports,
    clearSports,
    selectAllTeams,
    clearTeams,
    selectAllDays,
    clearDays,
    syncFilterDefaults
  }
})
