import api from '@/services/api'


export const getJudgesByEvent = async (eventId) => {
  const response = await api.get(`/events/${eventId}/judges`)
  return response.data
}


export const createJudge = async (eventId, payload) => {
  const response = await api.post(
    `/events/${eventId}/judges`,
    payload
  )
  return response.data
}


export const deleteJudge = async (judgeId) => {
  const response = await api.delete(`/judges/${judgeId}`)
  return response.data
}
