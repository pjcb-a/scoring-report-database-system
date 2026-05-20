/*
|--------------------------------------------------------------------------
| FORMAT DATE
|--------------------------------------------------------------------------
*/

export const formatDate = (

  value

) => {

  if (!value) {

    return 'N/A'
  }

  return new Date(value)
    .toLocaleDateString(
      'en-PH',
      {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }
    )
}


/*
|--------------------------------------------------------------------------
| FORMAT DATE TIME
|--------------------------------------------------------------------------
*/

export const formatDateTime = (

  value

) => {

  if (!value) {

    return 'N/A'
  }

  return new Date(value)
    .toLocaleString(
      'en-PH',
      {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit'
      }
    )
}


/*
|--------------------------------------------------------------------------
| FORMAT SCORE
|--------------------------------------------------------------------------
*/

export const formatScore = (

  value

) => {

  if (

    value === null ||
    value === undefined

  ) {

    return '0'
  }

  return Number(value)
    .toFixed(2)
}


/*
|--------------------------------------------------------------------------
| FORMAT PERCENTAGE
|--------------------------------------------------------------------------
*/

export const formatPercentage = (

  value

) => {

  if (

    value === null ||
    value === undefined

  ) {

    return '0%'
  }

  return (
    Number(value)
      .toFixed(2)
    + '%'
  )
}


/*
|--------------------------------------------------------------------------
| FORMAT STATUS
|--------------------------------------------------------------------------
*/

export const formatStatus = (

  value = ''

) => {

  return value
    .replaceAll('_', ' ')
    .toUpperCase()
}


/*
|--------------------------------------------------------------------------
| FORMAT RANK
|--------------------------------------------------------------------------
*/

export const formatRank = (

  rank

) => {

  if (rank === 1) {

    return '🥇 1st'
  }

  if (rank === 2) {

    return '🥈 2nd'
  }

  if (rank === 3) {

    return '🥉 3rd'
  }

  return `#${rank}`
}


/*
|--------------------------------------------------------------------------
| FORMAT EVENT TITLE
|--------------------------------------------------------------------------
*/

export const formatEventTitle = (

  event

) => {

  if (!event) {

    return 'Unknown Event'
  }

  return (

    `${event.event_name}
     (${event.start_day}
     - ${event.end_day})`

  )
}