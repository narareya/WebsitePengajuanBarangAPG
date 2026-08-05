import api from './axios'

export default {
  getMyRequests() {
    return api.get('/requests/me')
  },
  getAll() {
    return api.get('/requests/')
  },
  getById(id) {
    return api.get(`/requests/${id}`)
  },
  create(data) {
    return api.post('/requests/', data)
  },
  updateItems(id, data) {
    return api.patch(`/requests/${id}/items`, data)
  },
  approve(id, status) {
    return api.patch(`/requests/${id}/approve`, { status })
  },
  delete(id) {
    return api.delete(`/requests/${id}`)
  }
}