<template>
  <div class="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 px-4">
    <div class="w-full max-w-sm rounded-lg bg-white p-6 shadow-xl">
      <div class="flex items-start gap-3">
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full"
          :class="danger ? 'bg-red-100 text-red-600' : 'bg-indigo-100 text-indigo-600'"
        >
          <component :is="danger ? AlertTriangle : HelpCircle" class="h-5 w-5" />
        </div>
        <div class="flex-1">
          <h3 class="text-base font-semibold text-gray-900">{{ title }}</h3>
          <p class="mt-1 text-sm text-gray-500">{{ message }}</p>
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-2">
        <button
          type="button"
          :disabled="loading"
          @click="$emit('cancel')"
          class="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          {{ cancelText }}
        </button>
        <button
          type="button"
          :disabled="loading"
          @click="$emit('confirm')"
          class="rounded-md px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
          :class="danger ? 'bg-red-600 hover:bg-red-500' : 'bg-indigo-600 hover:bg-indigo-500'"
        >
          {{ loading ? 'Memproses...' : confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { AlertTriangle, HelpCircle } from 'lucide-vue-next'

defineProps({
  title: { type: String, required: true },
  message: { type: String, default: '' },
  confirmText: { type: String, default: 'Ya' },
  cancelText: { type: String, default: 'Batal' },
  danger: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
})
defineEmits(['confirm', 'cancel'])
</script>
