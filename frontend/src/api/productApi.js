import api from './axios'

export default {
  getAll() {
    return api.get('/products/')
  },
  getActive() {
    return api.get('/products/active')
  },
  getById(id) {
    return api.get(`/products/${id}`)
  },
  create(data) {
    return api.post('/products/', data)
  },
  update(id, data) {
    return api.patch(`/products/${id}`, data)
  },
  delete(id) {
    return api.delete(`/products/${id}`)
  }
}