import api from './axios'

export default {
  getAll(params = {}) {
    return api.get('/activity-logs/', { params })
  },
  export(params = {}) {
    return api.get('/activity-logs/export', { params, responseType: 'blob' })
  }
}