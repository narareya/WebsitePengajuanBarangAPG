<template>
    <div class="p-8">
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
            <History class="h-5 w-5" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Activity Log</h1>
            <p class="mt-0.5 text-sm text-gray-500">Riwayat aktivitas seluruh user</p>
          </div>
        </div>
        <button
          @click="handleExport"
          :disabled="exporting"
          class="flex items-center gap-1.5 rounded-md border border-gray-300 px-3 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:opacity-50"
        >
          <Download class="h-4 w-4" />
          {{ exporting ? 'Mengekspor...' : 'Export CSV' }}
        </button>
      </div>

      <div class="mb-4 flex flex-wrap items-end gap-3 rounded-lg border border-gray-200 bg-white p-3">
        <div class="min-w-[180px] flex-1">
          <label class="mb-1 block text-xs font-medium text-gray-500">Cari nama user</label>
          <input
            v-model="searchQuery"
            @keyup.enter="applyFilters"
            type="text"
            placeholder="Cari nama user..."
            class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-gray-500">Aksi</label>
          <select v-model="actionFilter" @change="applyFilters" class="rounded-md border border-gray-300 px-3 py-2 text-sm">
            <option value="">Semua Aksi</option>
            <option value="create">Create</option>
            <option value="update">Update</option>
            <option value="delete">Delete</option>
            <option value="approve">Approve</option>
            <option value="reject">Reject</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-gray-500">Entity</label>
          <select v-model="entityFilter" @change="applyFilters" class="rounded-md border border-gray-300 px-3 py-2 text-sm">
            <option value="">Semua Entity</option>
            <option value="request">Pengajuan</option>
            <option value="product">Produk</option>
            <option value="department">Department</option>
            <option value="user">User</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-gray-500">Dari Tanggal</label>
          <input v-model="startDate" @change="applyFilters" type="date" class="rounded-md border border-gray-300 px-3 py-2 text-sm" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-gray-500">Sampai Tanggal</label>
          <input v-model="endDate" @change="applyFilters" type="date" class="rounded-md border border-gray-300 px-3 py-2 text-sm" />
        </div>
        <button
          v-if="searchQuery || actionFilter || entityFilter || startDate || endDate"
          @click="resetFilters"
          class="rounded-md px-3 py-2 text-sm font-medium text-gray-500 hover:text-gray-700"
        >
          Reset
        </button>
      </div>

      <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
      <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Waktu</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">User</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Aksi</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Entity</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Keterangan</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="logs.length === 0">
              <td colspan="5" class="px-4 py-6 text-center text-sm text-gray-400">Belum ada aktivitas</td>
            </tr>
            <tr v-for="log in logs" :key="log.log_id">
              <td class="px-4 py-3 text-sm text-gray-700">{{ formatDate(log.created_at) }}</td>
              <td class="px-4 py-3 text-sm text-gray-700">{{ log.user_name }}</td>
              <td class="px-4 py-3">
                <span class="rounded-full px-2 py-1 text-xs font-medium capitalize" :class="actionClass(log.action)">
                  {{ log.action }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm capitalize text-gray-500">{{ log.entity }}</td>
              <td class="px-4 py-3 text-sm text-gray-700">{{ log.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-4 flex items-center justify-between text-sm text-gray-600">
        <p>Halaman {{ currentPage }} dari {{ totalPages }}</p>
        <div class="flex gap-2">
          <button @click="prevPage" :disabled="currentPage === 1" class="rounded-md border px-3 py-1 disabled:opacity-40">←</button>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="rounded-md border px-3 py-1 disabled:opacity-40">→</button>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, onMounted } from 'vue'
  import { History, Download } from 'lucide-vue-next'
  import activityLogApi from '@/api/activityLogApi'
  import { downloadBlob } from '@/utils/download'
  import { useToastStore } from '@/stores/toast'

  const toast = useToastStore()
  const logs = ref([])
  const loading = ref(true)
  const exporting = ref(false)
  const searchQuery = ref('')
  const actionFilter = ref('')
  const entityFilter = ref('')
  const startDate = ref('')
  const endDate = ref('')
  const currentPage = ref(1)
  const totalPages = ref(1)

  const buildParams = () => {
    const params = {}
    if (actionFilter.value) params.action = actionFilter.value
    if (entityFilter.value) params.entity = entityFilter.value
    if (searchQuery.value) params.search = searchQuery.value
    if (startDate.value) params.start_date = startDate.value
    if (endDate.value) params.end_date = endDate.value
    return params
  }

  const fetchLogs = async () => {
    try {
      loading.value = true
      const params = { ...buildParams(), page: currentPage.value, limit: 10 }
      const res = await activityLogApi.getAll(params)
      logs.value = res.data.items
      totalPages.value = res.data.total_pages
    } catch (err) {
      console.error(err)
    } finally {
      loading.value = false
    }
  }

  const applyFilters = () => {
    currentPage.value = 1
    fetchLogs()
  }

  const resetFilters = () => {
    searchQuery.value = ''
    actionFilter.value = ''
    entityFilter.value = ''
    startDate.value = ''
    endDate.value = ''
    applyFilters()
  }

  const handleExport = async () => {
    try {
      exporting.value = true
      const res = await activityLogApi.export(buildParams())
      downloadBlob(res.data, 'activity_log.csv')
    } catch (err) {
      console.error(err)
      toast.error('Gagal mengekspor activity log')
    } finally {
      exporting.value = false
    }
  }

  const nextPage = () => { if (currentPage.value < totalPages.value) { currentPage.value++; fetchLogs() } }
  const prevPage = () => { if (currentPage.value > 1) { currentPage.value--; fetchLogs() } }

  const formatDate = (dateStr) => new Date(dateStr).toLocaleString('id-ID')

  const actionClass = (action) => ({
    create: 'bg-green-100 text-green-700',
    update: 'bg-blue-100 text-blue-700',
    delete: 'bg-red-100 text-red-700',
    approve: 'bg-emerald-100 text-emerald-700',
    reject: 'bg-orange-100 text-orange-700'
  }[action] || 'bg-gray-100 text-gray-600')

  onMounted(fetchLogs)
  </script>
