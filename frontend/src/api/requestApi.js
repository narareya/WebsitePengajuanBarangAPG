import api from './axios'

export default {
  getMyRequests() {
    return api.get('/requests/me', { params: { limit: 100 } })
  },
  getAll() {
    return api.get('/requests/', { params: { limit: 100 } })
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
  approve(id, status, reason) {
    return api.patch(`/requests/${id}/approve`, { status, reason })
  },
  delete(id) {
    return api.delete(`/requests/${id}`)
  },
  uploadAttachment(id, file) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post(`/requests/${id}/attachment`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  downloadAttachment(id) {
    return api.get(`/requests/${id}/attachment`, { responseType: 'blob' })
  }
}