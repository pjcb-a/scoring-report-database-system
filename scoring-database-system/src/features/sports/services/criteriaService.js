import api from '@/services/api'


export const getCriteriaByEventSport = async (eventSportId) => {
  const response = await api.get(
    `/event-sports/${eventSportId}/criteria`
  )
  return response.data
}


export const createCriteria = async (eventSportId, payload) => {
  const response = await api.post(
    `/event-sports/${eventSportId}/criteria`,
    payload
  )
  return response.data
}


export const updateCriteria = async (criteriaId, payload) => {
  const response = await api.put(
    `/criteria/${criteriaId}`,
    payload
  )
  return response.data
}


export const deleteCriteria = async (criteriaId) => {
  const response = await api.delete(`/criteria/${criteriaId}`)
  return response.data
}
