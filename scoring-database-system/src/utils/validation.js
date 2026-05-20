import { reactive } from 'vue'

export function createValidation() {

  const errors = reactive({})

  const setError = (

    field,
    message

  ) => {

    errors[field] = message
  }

  const clearError = (

    field

  ) => {

    delete errors[field]
  }

  const clearErrors = () => {

    Object.keys(errors).forEach(

      key => delete errors[key]
    )
  }

  const hasErrors = () => {

    return (
      Object.keys(errors).length > 0
    )
  }

  return {

    errors,

    setError,

    clearError,

    clearErrors,

    hasErrors
  }
}