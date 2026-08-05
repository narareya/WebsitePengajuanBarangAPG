<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="w-full max-w-lg rounded-lg bg-white p-6">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Detail Pengajuan #{{ requestId }}</h2>
          <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
  
        <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
        <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>
  
        <div v-else>
          <div class="mb-4 grid grid-cols-2 gap-3 rounded-md bg-gray-50 p-3 text-sm">
            <div>
              <p class="text-gray-500">Tanggal</p>
              <p class="font-medium text-gray-900">{{ formatDate(detail.request_date) }}</p>
            </div>
            <div>
              <p class="text-gray-500">Status</p>
              <span class="rounded-full px-2 py-0.5 text-xs font-medium" :class="statusClass(detail.status)">
                {{ detail.status }}
              </span>
            </div>
            <div v-if="detail.approved_by">
              <p class="text-gray-500">Diproses oleh</p>
              <p class="font-medium text-gray-900">User #{{ detail.approved_by }}</p>
            </div>
            <div v-if="detail.approved_at">
              <p class="text-gray-500">Tanggal diproses</p>
              <p class="font-medium text-gray-900">{{ formatDate(detail.approved_at) }}</p>
            </div>
          </div>
  
          <p class="mb-2 text-sm font-semibold text-gray-700">Barang yang diminta</p>
          <div class="overflow-hidden rounded-md border border-gray-200">
            <table class="min-w-full divide-y divide-gray-200 text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-3 py-2 text-left text-xs font-semibold uppercase text-gray-500">Produk</th>
                  <th class="px-3 py-2 text-right text-xs font-semibold uppercase text-gray-500">Qty</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-if="!detail.details || detail.details.length === 0">
                  <td colspan="2" class="px-3 py-4 text-center text-gray-400">Tidak ada barang</td>
                </tr>
                <tr v-for="item in detail.details" :key="item.detail_id">
                  <td class="px-3 py-2 text-gray-700">{{ item.product_name }}</td>
                  <td class="px-3 py-2 text-right text-gray-700">{{ item.quantity }}</td>
                </tr>
              </tbody>
            </table>
          </div>
  
          <div class="mt-4">
            <p class="mb-2 text-sm font-semibold text-gray-700">Lampiran</p>
            <div v-if="detail.attachment_name" class="flex items-center justify-between rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm">
              <span class="flex items-center gap-2 truncate text-gray-700">
                <Paperclip class="h-4 w-4 shrink-0 text-gray-400" />
                <span class="truncate">{{ detail.attachment_name }}</span>
              </span>
              <button
                @click="handleDownload"
                :disabled="downloading"
                class="ml-3 shrink-0 text-sm font-medium text-indigo-600 hover:text-indigo-500 disabled:opacity-50"
              >
                {{ downloading ? 'Mengunduh...' : 'Unduh' }}
              </button>
            </div>
            <p v-else class="text-sm text-gray-400">Belum ada lampiran</p>

            <div v-if="canUpload" class="mt-2 flex items-center gap-2">
              <input
                ref="fileInputRef"
                type="file"
                @change="handleFileChange"
                class="block w-full text-xs text-gray-500 file:mr-3 file:rounded-md file:border-0 file:bg-indigo-50 file:px-3 file:py-1.5 file:text-xs file:font-medium file:text-indigo-600 hover:file:bg-indigo-100"
              />
              <button
                v-if="selectedFile"
                @click="handleUpload"
                :disabled="uploading"
                class="shrink-0 rounded-md bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50"
              >
                {{ uploading ? 'Mengunggah...' : 'Unggah' }}
              </button>
            </div>
            <p v-if="uploadError" class="mt-1 text-xs text-red-500">{{ uploadError }}</p>
          </div>

          <p v-if="actionError" class="mt-3 text-sm text-red-500">{{ actionError }}</p>

          <div v-if="showRejectReason" class="mt-4 rounded-md border border-red-200 bg-red-50 p-3">
            <label class="mb-1 block text-sm font-medium text-gray-700">Alasan reject</label>
            <textarea
              v-model="rejectReason"
              rows="2"
              class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-red-500 focus:outline-none"
              placeholder="Tulis alasan reject..."
            ></textarea>
            <div class="mt-2 flex justify-end gap-2">
              <button
                @click="showRejectReason = false"
                :disabled="processing"
                class="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-50"
              >
                Batal
              </button>
              <button
                @click="handleApprove('rejected', rejectReason)"
                :disabled="processing || !rejectReason.trim()"
                class="rounded-md bg-red-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50"
              >
                {{ processing ? 'Memproses...' : 'Konfirmasi Reject' }}
              </button>
            </div>
          </div>

          <div v-else-if="canApprove" class="mt-5 flex justify-end gap-2">
            <button
              @click="showRejectReason = true"
              :disabled="processing"
              class="rounded-md border border-red-300 px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-50 disabled:opacity-50"
            >
              Reject
            </button>
            <button
              @click="handleApprove('approved')"
              :disabled="processing"
              class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-50"
            >
              {{ processing ? 'Memproses...' : 'Approve' }}
            </button>
          </div>
  
          <div v-else class="mt-5 flex justify-end">
            <button
              @click="$emit('close')"
              type="button"
              class="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50"
            >
              Tutup
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { Paperclip } from 'lucide-vue-next'
  import requestApi from '@/api/requestApi'
  import { useAuthStore } from '@/stores/auth'

  const props = defineProps({
    requestId: { type: Number, required: true }
  })
  const emit = defineEmits(['close', 'updated'])

  const authStore = useAuthStore()

  const detail = ref(null)
  const loading = ref(true)
  const error = ref(null)
  const processing = ref(false)
  const actionError = ref(null)
  const showRejectReason = ref(false)
  const rejectReason = ref('')

  const fileInputRef = ref(null)
  const selectedFile = ref(null)
  const uploading = ref(false)
  const downloading = ref(false)
  const uploadError = ref(null)

  const canApprove = computed(() =>
    authStore.role === 'manager' && detail.value?.status === 'pending'
  )

  const canUpload = computed(() =>
    detail.value?.status === 'pending' && detail.value?.user_id === authStore.user?.user_id
  )
  
  const fetchDetail = async () => {
    try {
      loading.value = true
      const res = await requestApi.getById(props.requestId)
      detail.value = res.data
    } catch (err) {
      console.error(err)
      error.value = 'Gagal memuat detail pengajuan'
    } finally {
      loading.value = false
    }
  }
  
  const handleApprove = async (status, reason) => {
    actionError.value = null
    try {
      processing.value = true
      await requestApi.approve(props.requestId, status, reason)
      emit('updated')
      emit('close')
    } catch (err) {
      actionError.value = err.response?.data?.detail || 'Gagal memproses pengajuan'
    } finally {
      processing.value = false
    }
  }
  
  const handleFileChange = (e) => {
    selectedFile.value = e.target.files?.[0] || null
    uploadError.value = null
  }

  const handleUpload = async () => {
    if (!selectedFile.value) return
    uploadError.value = null
    try {
      uploading.value = true
      const res = await requestApi.uploadAttachment(props.requestId, selectedFile.value)
      detail.value = res.data
      selectedFile.value = null
      if (fileInputRef.value) fileInputRef.value.value = ''
    } catch (err) {
      uploadError.value = err.response?.data?.detail || 'Gagal mengunggah lampiran'
    } finally {
      uploading.value = false
    }
  }

  const handleDownload = async () => {
    try {
      downloading.value = true
      const res = await requestApi.downloadAttachment(props.requestId)
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = detail.value.attachment_name
      link.click()
      window.URL.revokeObjectURL(url)
    } catch (err) {
      console.error(err)
    } finally {
      downloading.value = false
    }
  }

  const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    return new Date(dateStr).toLocaleDateString('id-ID', {
      day: '2-digit', month: 'short', year: 'numeric'
    })
  }
  
  const statusClass = (status) => {
    return {
      pending: 'bg-yellow-100 text-yellow-700',
      approved: 'bg-green-100 text-green-700',
      rejected: 'bg-red-100 text-red-700'
    }[status] || 'bg-gray-100 text-gray-600'
  }
  
  onMounted(fetchDetail)
  </script>