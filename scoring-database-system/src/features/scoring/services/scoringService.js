import api from '@/services/api'


export const getScoresByEvent = async (eventId) => {
  const response = await api.get(`/events/${eventId}/scores`)
  return response.data
}


export const finalizeMatch = async (gameId, payload) => {
  const response = await api.post(`/games/${gameId}/finalize`, payload)
  return response.data
}
