<template>
    <div class="p-8">
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Pengajuan</h1>
          <p class="mt-1 text-sm text-gray-500">{{ pageSubtitle }}</p>
        </div>
        <button
          v-if="authStore.role === 'employee'"
          @click="openCreate"
          class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          + Buat Pengajuan
        </button>
      </div>
  
      <div class="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div class="relative w-full sm:max-w-xs">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari ID atau nama pemohon..."
            class="w-full rounded-md border border-gray-300 py-2 pl-9 pr-3 text-sm focus:border-indigo-500 focus:outline-none"
          />
          <svg class="absolute left-3 top-2.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
          </svg>
        </div>
  
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-500">Status:</label>
          <select
            v-model="statusFilter"
            class="rounded-md border border-gray-300 py-2 px-3 text-sm focus:border-indigo-500 focus:outline-none"
          >
            <option value="all">Semua</option>
            <option value="pending">Menunggu</option>
            <option value="approved">Disetujui</option>
            <option value="rejected">Ditolak</option>
          </select>
        </div>
      </div>
  
      <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
      <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>
  
      <template v-else>
        <p v-if="filteredRequests.length === 0" class="rounded-md border border-gray-200 bg-white py-10 text-center text-sm text-gray-400">
          Tidak ada pengajuan yang cocok.
        </p>
  
        <RequestTable
          v-else
          :requests="paginatedRequests"
          @detail="openDetail"
          @edit="openEdit"
          @delete="handleDelete"
        />
  
        <div v-if="filteredRequests.length > 0" class="mt-4 flex items-center justify-between">
          <p class="text-sm text-gray-500">
            Menampilkan {{ startIndex + 1 }}-{{ endIndex }} dari {{ filteredRequests.length }} pengajuan
          </p>
          <div class="flex items-center gap-1">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Prev
            </button>
            <button
              v-for="page in totalPages"
              :key="page"
              @click="currentPage = page"
              class="rounded-md px-3 py-1.5 text-sm font-medium"
              :class="page === currentPage
                ? 'bg-indigo-600 text-white'
                : 'border border-gray-300 text-gray-600 hover:bg-gray-50'"
            >
              {{ page }}
            </button>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="rounded-md border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-600 hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      </template>
  
      <RequestFormModal
        v-if="showForm"
        :products="products"
        :request-data="editingRequest"
        @close="closeForm"
        @submitted="fetchRequests"
      />
  
      <RequestDetailModal
        v-if="selectedRequestId"
        :request-id="selectedRequestId"
        @close="selectedRequestId = null"
        @updated="fetchRequests"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed, watch } from 'vue'
  import requestApi from '@/api/requestApi'
  import productApi from '@/api/productApi'
  import { useAuthStore } from '@/stores/auth'
  import RequestTable from '@/components/request/RequestTable.vue'
  import RequestFormModal from '@/components/request/RequestFormModal.vue'
  import RequestDetailModal from '@/components/request/RequestDetailModal.vue'
  
  const authStore = useAuthStore()
  const requests = ref([])
  const products = ref([])
  const loading = ref(true)
  const error = ref(null)
  const showForm = ref(false)
  const selectedRequestId = ref(null)
  
  const searchQuery = ref('')
  const statusFilter = ref('all')
  const currentPage = ref(1)
  const pageSize = 10
  
  const pageSubtitle = computed(() =>
    authStore.role === 'employee'
      ? 'Daftar pengajuan barang milikmu'
      : 'Daftar seluruh pengajuan barang',
  )
  
  const fetchRequests = async () => {
    try {
      loading.value = true
      const res =
        authStore.role === 'employee' ? await requestApi.getMyRequests() : await requestApi.getAll()
      requests.value = res.data
    } catch (err) {
      console.error(err)
      error.value = 'Gagal memuat data pengajuan'
    } finally {
      loading.value = false
    }
  }
  
  const fetchProducts = async () => {
    try {
      const res = await productApi.getActive()
      products.value = res.data
    } catch (err) {
      console.error(err)
    }
  }
  
  const filteredRequests = computed(() => {
    let result = requests.value
  
    if (statusFilter.value !== 'all') {
      result = result.filter((r) => r.status === statusFilter.value)
    }
  
    const q = searchQuery.value.trim().toLowerCase()
    if (q) {
      result = result.filter((r) => {
        const idMatch = String(r.request_id).includes(q)
        const nameMatch = r.user?.name?.toLowerCase().includes(q) || r.actor?.toLowerCase().includes(q)
        return idMatch || nameMatch
      })
    }
  
    return result
  })
  
  const totalPages = computed(() =>
    Math.max(1, Math.ceil(filteredRequests.value.length / pageSize))
  )
  
  const startIndex = computed(() => (currentPage.value - 1) * pageSize)
  const endIndex = computed(() =>
    Math.min(startIndex.value + pageSize, filteredRequests.value.length)
  )
  
  const paginatedRequests = computed(() =>
    filteredRequests.value.slice(startIndex.value, startIndex.value + pageSize)
  )
  
  watch([searchQuery, statusFilter], () => {
    currentPage.value = 1
  })
  
  watch(totalPages, (newTotal) => {
    if (currentPage.value > newTotal) {
      currentPage.value = newTotal
    }
  })
  
  const handleDelete = async (id) => {
    if (!confirm('Yakin mau hapus pengajuan ini?')) return
    try {
      await requestApi.delete(id)
      await fetchRequests()
    } catch (err) {
      alert(err.response?.data?.detail || 'Gagal menghapus pengajuan')
    }
  }
  
  const openDetail = (id) => {
    selectedRequestId.value = id
  }
  
  const editingRequest = ref(null)
  
  const openCreate = () => {
    editingRequest.value = null
    showForm.value = true
  }
  
  const openEdit = async (request) => {
    const res = await requestApi.getById(request.request_id)
    editingRequest.value = res.data
    showForm.value = true
  }
  
  const closeForm = () => {
    showForm.value = false
    editingRequest.value = null
  }
  
  onMounted(() => {
    fetchRequests()
    fetchProducts()
  })
  </script>