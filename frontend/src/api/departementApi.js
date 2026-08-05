import api from './axios'

export default {
  getAll() {
    return api.get('/departements/')
  },
  getById(id) {
    return api.get(`/departements/${id}`)
  },
  create(data) {
    return api.post('/departements/', data)
  },
  update(id, data) {
    return api.patch(`/departements/${id}`, data)
  },
  delete(id) {
    return api.delete(`/departements/${id}`)
  }
}