<template>
  <div class="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 px-4">
    <div class="w-full max-w-sm rounded-lg bg-white p-6 shadow-xl">
      <h3 class="text-base font-semibold text-gray-900">{{ title }}</h3>
      <p class="mt-1 text-sm text-gray-500">Alasan reject wajib diisi.</p>

      <textarea
        v-model="reason"
        rows="3"
        autofocus
        class="mt-3 w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-red-500 focus:outline-none"
        placeholder="Tulis alasan reject..."
      ></textarea>

      <div class="mt-4 flex justify-end gap-2">
        <button
          type="button"
          :disabled="loading"
          @click="$emit('cancel')"
          class="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 disabled:opacity-50"
        >
          Batal
        </button>
        <button
          type="button"
          :disabled="loading || !reason.trim()"
          @click="$emit('confirm', reason.trim())"
          class="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50"
        >
          {{ loading ? 'Memproses...' : 'Konfirmasi Reject' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  title: { type: String, default: 'Reject pengajuan?' },
  loading: { type: Boolean, default: false },
})
defineEmits(['confirm', 'cancel'])

const reason = ref('')
</script>
