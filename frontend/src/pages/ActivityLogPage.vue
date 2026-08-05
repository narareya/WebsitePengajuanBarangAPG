<template>
    <div class="p-8">
      <div class="mb-6 flex items-center gap-3">
        <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
          <History class="h-5 w-5" />
        </div>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Activity Log</h1>
          <p class="mt-0.5 text-sm text-gray-500">Riwayat aktivitas seluruh user</p>
        </div>
      </div>
  
      <div class="mb-4 flex gap-3">
        <input
          v-model="searchQuery"
          @keyup.enter="fetchLogs"
          type="text"
          placeholder="Cari nama user..."
          class="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm"
        />
        <select v-model="actionFilter" @change="fetchLogs" class="rounded-md border border-gray-300 px-3 py-2 text-sm">
          <option value="">Semua Aksi</option>
          <option value="create">Create</option>
          <option value="update">Update</option>
          <option value="delete">Delete</option>
          <option value="approve">Approve</option>
          <option value="reject">Reject</option>
        </select>
      </div>
  
      <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
      <div v-else class="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Waktu</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">User</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Aksi</th>
              <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Keterangan</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="logs.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-sm text-gray-400">Belum ada aktivitas</td>
            </tr>
            <tr v-for="log in logs" :key="log.log_id">
              <td class="px-4 py-3 text-sm text-gray-700">{{ formatDate(log.created_at) }}</td>
              <td class="px-4 py-3 text-sm text-gray-700">{{ log.user_name }}</td>
              <td class="px-4 py-3">
                <span class="rounded-full px-2 py-1 text-xs font-medium capitalize" :class="actionClass(log.action)">
                  {{ log.action }}
                </span>
              </td>
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
  import { History } from 'lucide-vue-next'
  import activityLogApi from '@/api/activityLogApi'
  
  const logs = ref([])
  const loading = ref(true)
  const searchQuery = ref('')
  const actionFilter = ref('')
  const currentPage = ref(1)
  const totalPages = ref(1)
  
  const fetchLogs = async () => {
    try {
      loading.value = true
      const params = { page: currentPage.value, limit: 10 }
      if (actionFilter.value) params.action = actionFilter.value
      if (searchQuery.value) params.search = searchQuery.value
  
      const res = await activityLogApi.getAll(params)
      logs.value = res.data.items
      totalPages.value = res.data.total_pages
    } catch (err) {
      console.error(err)
    } finally {
      loading.value = false
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