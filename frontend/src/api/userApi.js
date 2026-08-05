import api from './axios'

export default {
  getAll() {
    return api.get('/users/')
  },
  getById(id) {
    return api.get(`/users/${id}`)
  },
  create(data) {
    return api.post('/users/', data)
  },
  update(id, data) {
    return api.patch(`/users/${id}`, data)
  },
  delete(id) {
    return api.delete(`/users/${id}`)
  }
}