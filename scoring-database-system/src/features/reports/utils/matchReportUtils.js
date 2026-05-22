export const COMPONENT_SCORE = 'Component Score'

export const getSportName = (match) =>
  match.sport || match.game_name || 'Unknown sport'

export const getTeamNames = (match) => {
  const names = new Set()

  for (const score of match.scores || []) {
    if (score.team) {
      names.add(score.team)
    }
  }

  for (const team of match.teams || []) {
    if (team.team_name) {
      names.add(team.team_name)
    }
  }

  return [...names]
}

export const getDateKey = (match) => {
  const raw = match.start_date || match.end_date

  if (!raw) {
    return 'undated'
  }

  return String(raw).split('T')[0]
}

export const formatDayLabel = (dateKey) => {
  if (dateKey === 'undated') {
    return 'No scheduled date'
  }

  const date = new Date(`${dateKey}T12:00:00`)

  if (Number.isNaN(date.getTime())) {
    return dateKey
  }

  return date.toLocaleDateString(undefined, {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

export const formatMatchDateTime = (match) => {
  const raw = match.start_date || match.end_date

  if (!raw) {
    return '—'
  }

  const date = new Date(raw)

  if (Number.isNaN(date.getTime())) {
    return raw
  }

  return date.toLocaleString()
}

const getTeamSortKey = (match) =>
  getTeamNames(match).sort().join(', ').toLowerCase()

export const compareMatches = (a, b, sortBy, sortDirection) => {
  const direction = sortDirection === 'asc' ? 1 : -1

  if (sortBy === 'sport') {
    return (
      getSportName(a).localeCompare(getSportName(b)) * direction
    )
  }

  if (sortBy === 'team') {
    return (
      getTeamSortKey(a).localeCompare(getTeamSortKey(b)) * direction
    )
  }

  const dateA = getDateKey(a)
  const dateB = getDateKey(b)

  if (dateA === 'undated' && dateB === 'undated') {
    return 0
  }

  if (dateA === 'undated') {
    return 1
  }

  if (dateB === 'undated') {
    return -1
  }

  if (dateA < dateB) {
    return -1 * direction
  }

  if (dateA > dateB) {
    return 1 * direction
  }

  return getSportName(a).localeCompare(getSportName(b))
}
