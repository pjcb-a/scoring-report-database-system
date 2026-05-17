import api from '@/services/api'

export const getEvents = async () => {
  const response = await api.get('/events')
  return response.data
}

export const createEvent = async (payload) => {
  const response = await api.post('/events', payload)
  return response.data
}