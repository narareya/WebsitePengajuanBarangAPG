import { defineStore } from 'pinia'

let nextId = 1

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),
  actions: {
    show(message, type = 'error', duration = 4000) {
      const id = nextId++
      this.toasts.push({ id, message, type })
      setTimeout(() => this.dismiss(id), duration)
      return id
    },
    error(message) {
      return this.show(message, 'error')
    },
    success(message) {
      return this.show(message, 'success')
    },
    dismiss(id) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
  },
})
