<template>
    <div class="p-8">
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Master Product</h1>
          <p class="mt-1 text-sm text-gray-500">Kelola daftar produk</p>
        </div>
        <button @click="openCreate" class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500">
          + Tambah Produk
        </button>
      </div>
  
      <div class="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div class="relative w-full sm:max-w-xs">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari nama produk..."
            class="w-full rounded-md border border-gray-300 py-2 pl-9 pr-3 text-sm focus:border-indigo-500 focus:outline-none"
          />
          <svg class="absolute left-3 top-2.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
          </svg>
        </div>
  
        <select v-model="statusFilter" class="rounded-md border border-gray-300 py-2 px-3 text-sm focus:border-indigo-500 focus:outline-none">
          <option value="all">Semua Status</option>
          <option value="active">Aktif</option>
          <option value="inactive">Nonaktif</option>
        </select>
      </div>
  
      <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
      <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>
  
      <template v-else>
        <p v-if="filteredProducts.length === 0" class="rounded-md border border-gray-200 bg-white py-10 text-center text-sm text-gray-400">
          Tidak ada produk yang cocok.
        </p>
  
        <ProductTable v-else :products="paginatedProducts" @edit="openEdit" @delete="handleDelete" />
  
        <div v-if="filteredProducts.length > 0" class="mt-4 flex items-center justify-between">
          <p class="text-sm text-gray-500">
            Menampilkan {{ startIndex + 1 }}-{{ endIndex }} dari {{ filteredProducts.length }} produk
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
              :class="page === currentPage ? 'bg-indigo-600 text-white' : 'border border-gray-300 text-gray-600 hover:bg-gray-50'"
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
  
      <ProductFormModal
        v-if="showForm"
        :product="selectedProduct"
        @close="closeForm"
        @saved="fetchProducts"
      />

      <ConfirmDialog
        v-if="showDeleteConfirm"
        title="Hapus produk ini?"
        message="Produk yang dihapus tidak bisa dikembalikan."
        confirm-text="Hapus"
        danger
        :loading="deleting"
        @confirm="confirmDelete"
        @cancel="showDeleteConfirm = false"
      />
    </div>
  </template>

  <script setup>
  import { ref, onMounted, computed, watch } from 'vue'
  import productApi from '@/api/productApi'
  import ProductTable from '@/components/products/ProductTable.vue'
  import ProductFormModal from '@/components/products/ProductFormModal.vue'
  import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
  
  const products = ref([])
  const loading = ref(true)
  const error = ref(null)
  const showForm = ref(false)
  const selectedProduct = ref(null)
  
  const searchQuery = ref('')
  const statusFilter = ref('all')
  const currentPage = ref(1)
  const pageSize = 10
  
  const fetchProducts = async () => {
    try {
      loading.value = true
      const res = await productApi.getAll()
      products.value = res.data
    } catch (err) {
      console.error(err)
      error.value = 'Gagal memuat data produk'
    } finally {
      loading.value = false
    }
  }
  
  const filteredProducts = computed(() => {
    let result = products.value
  
    if (statusFilter.value !== 'all') {
      const wantActive = statusFilter.value === 'active'
      result = result.filter((p) => Boolean(p.is_active) === wantActive)
    }
  
    const q = searchQuery.value.trim().toLowerCase()
    if (q) {
      result = result.filter((p) => p.name?.toLowerCase().includes(q))
    }
  
    return result
  })
  
  const totalPages = computed(() => Math.max(1, Math.ceil(filteredProducts.value.length / pageSize)))
  const startIndex = computed(() => (currentPage.value - 1) * pageSize)
  const endIndex = computed(() => Math.min(startIndex.value + pageSize, filteredProducts.value.length))
  const paginatedProducts = computed(() => filteredProducts.value.slice(startIndex.value, startIndex.value + pageSize))
  
  watch([searchQuery, statusFilter], () => {
    currentPage.value = 1
  })
  watch(totalPages, (newTotal) => {
    if (currentPage.value > newTotal) currentPage.value = newTotal
  })
  
  const openCreate = () => {
    selectedProduct.value = null
    showForm.value = true
  }
  
  const openEdit = (product) => {
    selectedProduct.value = product
    showForm.value = true
  }
  
  const closeForm = () => {
    showForm.value = false
    selectedProduct.value = null
  }
  
  const showDeleteConfirm = ref(false)
  const deleting = ref(false)
  const pendingDeleteId = ref(null)

  const handleDelete = (id) => {
    pendingDeleteId.value = id
    showDeleteConfirm.value = true
  }

  const confirmDelete = async () => {
    try {
      deleting.value = true
      await productApi.delete(pendingDeleteId.value)
      showDeleteConfirm.value = false
      await fetchProducts()
    } catch (err) {
      alert(err.response?.data?.detail || 'Gagal menghapus produk')
    } finally {
      deleting.value = false
    }
  }

  onMounted(fetchProducts)
  </script>