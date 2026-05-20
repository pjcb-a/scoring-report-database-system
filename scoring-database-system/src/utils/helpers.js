/*
|--------------------------------------------------------------------------
| GENERATE RANDOM ID
|--------------------------------------------------------------------------
*/

export const generateId = () => {

  return (
    Date.now().toString(36) +
    Math.random()
      .toString(36)
      .substring(2, 9)
  )
}


/*
|--------------------------------------------------------------------------
| CAPITALIZE
|--------------------------------------------------------------------------
*/

export const capitalize = (

  value = ''

) => {

  if (!value) {

    return ''
  }

  return (

    value.charAt(0)
      .toUpperCase()

    +

    value.slice(1)
  )
}


/*
|--------------------------------------------------------------------------
| TRUNCATE TEXT
|--------------------------------------------------------------------------
*/

export const truncate = (

  value = '',

  length = 50

) => {

  if (

    value.length <= length

  ) {

    return value
  }

  return (
    value.substring(0, length)
    + '...'
  )
}


/*
|--------------------------------------------------------------------------
| DEBOUNCE
|--------------------------------------------------------------------------
*/

export const debounce = (

  callback,

  delay = 300

) => {

  let timeout

  return (...args) => {

    clearTimeout(timeout)

    timeout = setTimeout(() => {

      callback(...args)

    }, delay)
  }
}


/*
|--------------------------------------------------------------------------
| DEEP CLONE
|--------------------------------------------------------------------------
*/

export const deepClone = (

  value

) => {

  return JSON.parse(
    JSON.stringify(value)
  )
}


/*
|--------------------------------------------------------------------------
| EMPTY CHECK
|--------------------------------------------------------------------------
*/

export const isEmpty = (

  value

) => {

  if (

    value === null ||
    value === undefined

  ) {

    return true
  }

  if (

    typeof value === 'string'

  ) {

    return value.trim() === ''
  }

  if (

    Array.isArray(value)

  ) {

    return value.length === 0
  }

  if (

    typeof value === 'object'

  ) {

    return (
      Object.keys(value).length === 0
    )
  }

  return false
}