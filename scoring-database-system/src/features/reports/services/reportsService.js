import api from '@/services/api'


export const getMatchReports = async (eventId) => {
  const response = await api.get(
    `/events/${eventId}/reports/matches`
  )
  return response.data
}
