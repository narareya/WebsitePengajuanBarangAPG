<template>
  <div class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">ID</th>
          <th v-if="!canEdit" class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Pemohon</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Tanggal</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Lampiran</th>
          <th class="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">Aksi</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-if="requests.length === 0">
          <td :colspan="canEdit ? 5 : 6" class="px-4 py-8 text-center text-sm text-gray-400">
            Belum ada pengajuan
          </td>
        </tr>
        <tr v-for="req in requests" :key="req.request_id" class="transition-colors hover:bg-gray-50">
          <td class="px-4 py-3 text-sm font-medium text-gray-700">#{{ req.request_id }}</td>
          <td v-if="!canEdit" class="px-4 py-3 text-sm text-gray-700">{{ req.user_name || '-' }}</td>
          <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(req.request_date) }}</td>
          <td class="px-4 py-3">
            <span
              class="inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium"
              :class="statusClass(req.status)"
            >
              {{ statusLabel(req.status) }}
            </span>
          </td>
          <td class="px-4 py-3 text-sm text-gray-400">
            <Paperclip v-if="req.attachment_name" class="h-4 w-4 text-gray-400" />
            <span v-else>-</span>
          </td>
          <td class="px-4 py-3 text-right">
            <button
              @click="$emit('detail', req.request_id)"
              class="text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              Detail
            </button>
            <button
              v-if="req.status === 'pending' && canEdit"
              @click="$emit('edit', req)"
              class="ml-3 text-sm font-medium text-indigo-600 hover:text-indigo-500"
            >
              Edit
            </button>
            <button
              v-if="req.status === 'pending' && canEdit"
              @click="$emit('delete', req.request_id)"
              class="ml-3 text-sm font-medium text-red-500 hover:text-red-400"
            >
              Hapus
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { Paperclip } from 'lucide-vue-next'

defineProps({ requests: { type: Array, required: true } })
defineEmits(['detail', 'edit','delete'])

import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
const canEdit = authStore.role === 'employee'

const statusLabel = (status) => {
  return { pending: 'Menunggu', approved: 'Disetujui', rejected: 'Ditolak' }[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

const statusClass = (status) => {
  return (
    {
      pending: 'bg-yellow-100 text-yellow-700',
      approved: 'bg-green-100 text-green-700',
      rejected: 'bg-red-100 text-red-700',
    }[status] || 'bg-gray-100 text-gray-600'
  )
}
</script>
