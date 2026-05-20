/*
|--------------------------------------------------------------------------
| REQUIRED
|--------------------------------------------------------------------------
*/

export const required = (

  value,

  label = 'Field'

) => {

  if (

    value === null ||

    value === undefined ||

    value === ''

  ) {

    return `${label} is required.`
  }

  return ''
}


/*
|--------------------------------------------------------------------------
| MIN LENGTH
|--------------------------------------------------------------------------
*/

export const minLength = (

  value,

  length,

  label = 'Field'

) => {

  if (

    value &&
    value.length < length

  ) {

    return `${label} must be at least ${length} characters.`
  }

  return ''
}


/*
|--------------------------------------------------------------------------
| MAX LENGTH
|--------------------------------------------------------------------------
*/

export const maxLength = (

  value,

  length,

  label = 'Field'

) => {

  if (

    value &&
    value.length > length

  ) {

    return `${label} must not exceed ${length} characters.`
  }

  return ''
}

/*
|--------------------------------------------------------------------------
| POSITIVE NUMBER
|--------------------------------------------------------------------------
*/

export const positiveNumber = (

  value,

  label = 'Value'

) => {

  if (

    Number(value) < 0

  ) {

    return `${label} must be positive.`
  }

  return ''
}


/*
|--------------------------------------------------------------------------
| HEX COLOR
|--------------------------------------------------------------------------
*/

export const hexColor = (

  value,

  label = 'Color'

) => {

  const regex =
    /^#([0-9A-F]{3}){1,2}$/i

  if (

    value &&
    !regex.test(value)

  ) {

    return `${label} must be a valid hex color.`
  }

  return ''
}


/*
|--------------------------------------------------------------------------
| DATE RANGE
|--------------------------------------------------------------------------
*/

export const validDateRange = (

  startDate,

  endDate

) => {

  if (

    startDate &&
    endDate &&
    new Date(startDate)
      >
    new Date(endDate)

  ) {

    return 'End date must be after start date.'
  }

  return ''
}