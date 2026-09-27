<template>
  <div class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">No.</th>
          <th v-if="!canEdit" class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Pemohon</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Barang</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Tanggal</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
          <th class="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Lampiran</th>
          <th class="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">Aksi</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-100">
        <tr v-if="requests.length === 0">
          <td :colspan="canEdit ? 6 : 7" class="px-4 py-8 text-center text-sm text-gray-400">
            Belum ada pengajuan
          </td>
        </tr>
        <tr v-for="(req, index) in requests" :key="req.request_id" class="transition-colors hover:bg-gray-50">
          <td class="px-4 py-3 text-sm font-medium text-gray-700">{{ startIndex + index + 1 }}</td>
          <td v-if="!canEdit" class="px-4 py-3 text-sm text-gray-700">{{ req.user_name || '-' }}</td>
          <td class="max-w-xs px-4 py-3 text-sm text-gray-700">
            <span class="inline-flex items-center gap-1.5">
              <span class="truncate" :title="req.items_summary">{{ req.items_summary || '-' }}</span>
              <span
                v-if="req.stock_warning"
                title="Stok tidak cukup untuk salah satu barang"
                class="inline-flex shrink-0 items-center gap-1 rounded-full bg-red-100 px-1.5 py-0.5 text-[10px] font-medium text-red-700"
              >
                <AlertTriangle class="h-3 w-3" />
                Stok kurang
              </span>
            </span>
          </td>
          <td class="px-4 py-3 text-sm text-gray-500">{{ formatDate(req.request_date) }}</td>
          <td class="px-4 py-3">
            <span
              class="inline-flex items-center gap-1 rounded-full px-2 py-1 text-xs font-medium"
              :class="statusClass(req.status)"
            >
              {{ statusLabel(req.status) }}
            </span>
          </td>
          <td class="px-4 py-3 text-sm">
            <button
              v-if="req.attachment_name"
              @click="openZoom(req)"
              title="Klik untuk lihat lampiran"
              class="inline-flex items-center gap-1 text-indigo-600 hover:text-indigo-500"
            >
              <ImageIcon class="h-4 w-4" />
            </button>
            <span v-else class="text-gray-300">-</span>
          </td>
          <td class="px-4 py-3 text-right">
            <button
              v-if="req.status === 'pending' && canApprove"
              @click="$emit('approve', req.request_id)"
              title="Approve"
              class="inline-flex items-center gap-1 rounded-md bg-green-50 px-2.5 py-1 text-sm font-medium text-green-700 hover:bg-green-100"
            >
              <Check class="h-3.5 w-3.5" />
              Approve
            </button>
            <button
              v-if="req.status === 'pending' && canApprove"
              @click="$emit('reject', req.request_id)"
              title="Reject"
              class="ml-2 inline-flex items-center gap-1 rounded-md bg-red-50 px-2.5 py-1 text-sm font-medium text-red-600 hover:bg-red-100"
            >
              <X class="h-3.5 w-3.5" />
              Reject
            </button>
            <button
              @click="$emit('detail', req.request_id)"
              class="ml-3 text-sm font-medium text-indigo-600 hover:text-indigo-500"
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

    <ImageZoomModal
      v-if="zoomOpen"
      :image-url="zoomImageUrl"
      :filename="zoomFilename"
      :loading="zoomLoading"
      :error="zoomError"
      @close="closeZoom"
    />
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount } from 'vue'
import { Image as ImageIcon, Check, X, AlertTriangle } from 'lucide-vue-next'
import requestApi from '@/api/requestApi'
import ImageZoomModal from '@/components/common/ImageZoomModal.vue'

defineProps({
  requests: { type: Array, required: true },
  startIndex: { type: Number, default: 0 },
})
defineEmits(['detail', 'edit', 'delete', 'approve', 'reject'])

import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
const canEdit = authStore.role === 'employee'
const canApprove = authStore.role === 'manager' || authStore.role === 'admin'

const zoomOpen = ref(false)
const zoomImageUrl = ref(null)
const zoomFilename = ref('')
const zoomLoading = ref(false)
const zoomError = ref(null)

const openZoom = async (req) => {
  zoomOpen.value = true
  zoomFilename.value = req.attachment_name
  zoomLoading.value = true
  zoomError.value = null
  zoomImageUrl.value = null
  try {
    const res = await requestApi.downloadAttachment(req.request_id)
    zoomImageUrl.value = window.URL.createObjectURL(new Blob([res.data]))
  } catch (err) {
    zoomError.value = 'Gagal memuat lampiran'
  } finally {
    zoomLoading.value = false
  }
}

const closeZoom = () => {
  zoomOpen.value = false
  if (zoomImageUrl.value) window.URL.revokeObjectURL(zoomImageUrl.value)
  zoomImageUrl.value = null
}

onBeforeUnmount(() => {
  if (zoomImageUrl.value) window.URL.revokeObjectURL(zoomImageUrl.value)
})

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
