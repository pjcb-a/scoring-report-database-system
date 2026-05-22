export const EVENT_STATUS_OPTIONS = [
  { value: 'Upcoming', label: 'Upcoming' },
  { value: 'Ongoing', label: 'Ongoing' },
  { value: 'Completed', label: 'Completed' }
]

export const ALLOWED_EVENT_STATUSES = [
  'Upcoming',
  'Ongoing',
  'Completed'
]

export function normalizeEventStatus(status) {
  if (status === 'Active') {
    return 'Ongoing'
  }

  if (ALLOWED_EVENT_STATUSES.includes(status)) {
    return status
  }

  return 'Upcoming'
}

export function eventStatusBadgeClass(status) {
  const normalized = normalizeEventStatus(status)

  if (normalized === 'Ongoing') {
    return 'status-badge--ongoing'
  }

  if (normalized === 'Completed') {
    return 'status-badge--completed'
  }

  return 'status-badge--upcoming'
}
