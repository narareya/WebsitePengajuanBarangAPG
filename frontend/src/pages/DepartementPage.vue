<template>
    <div class="p-8">
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
            <Building2 class="h-5 w-5" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Master Department</h1>
            <p class="mt-0.5 text-sm text-gray-500">Kelola daftar department</p>
          </div>
        </div>
        <button @click="openCreate" class="flex items-center gap-1.5 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
          <Plus class="h-4 w-4" />
          Tambah Department
        </button>
      </div>
  
      <div class="mb-4 relative w-full sm:max-w-xs">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari nama department..."
          class="w-full rounded-md border border-gray-300 py-2 pl-9 pr-3 text-sm focus:border-indigo-500 focus:outline-none"
        />
        <svg class="absolute left-3 top-2.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
        </svg>
      </div>
  
      <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
      <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>
  
      <template v-else>
        <p v-if="filteredDepartments.length === 0" class="rounded-md border border-gray-200 bg-white py-10 text-center text-sm text-gray-400">
          Tidak ada department yang cocok.
        </p>
  
        <DepartementTable v-else :departments="paginatedDepartments" @edit="openEdit" @delete="handleDelete" />
  
        <div v-if="filteredDepartments.length > 0" class="mt-4 flex items-center justify-between">
          <p class="text-sm text-gray-500">
            Menampilkan {{ startIndex + 1 }}-{{ endIndex }} dari {{ filteredDepartments.length }} department
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
  
      <DepartementFormModal
        v-if="showForm"
        :department="selectedDepartment"
        @close="closeForm"
        @saved="fetchDepartments"
      />

      <ConfirmDialog
        v-if="showDeleteConfirm"
        title="Hapus department ini?"
        message="Department yang dihapus tidak bisa dikembalikan."
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
  import { Building2, Plus } from 'lucide-vue-next'
  import departementApi from '@/api/departementApi'
  import DepartementTable from '@/components/departement/DepartementTable.vue'
  import DepartementFormModal from '@/components/departement/DepartementFormModal.vue'
  import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
  
  const departments = ref([])
  const loading = ref(true)
  const error = ref(null)
  const showForm = ref(false)
  const selectedDepartment = ref(null)
  
  const searchQuery = ref('')
  const currentPage = ref(1)
  const pageSize = 10
  
  const fetchDepartments = async () => {
    try {
      loading.value = true
      const res = await departementApi.getAll()
      departments.value = res.data
    } catch (err) {
      console.error(err)
      error.value = 'Gagal memuat data department'
    } finally {
      loading.value = false
    }
  }
  
  const filteredDepartments = computed(() => {
    const q = searchQuery.value.trim().toLowerCase()
    if (!q) return departments.value
    return departments.value.filter((d) => d.departement_name?.toLowerCase().includes(q))
  })
  
  const totalPages = computed(() => Math.max(1, Math.ceil(filteredDepartments.value.length / pageSize)))
  const startIndex = computed(() => (currentPage.value - 1) * pageSize)
  const endIndex = computed(() => Math.min(startIndex.value + pageSize, filteredDepartments.value.length))
  const paginatedDepartments = computed(() => filteredDepartments.value.slice(startIndex.value, startIndex.value + pageSize))
  
  watch(searchQuery, () => {
    currentPage.value = 1
  })
  watch(totalPages, (newTotal) => {
    if (currentPage.value > newTotal) currentPage.value = newTotal
  })
  
  const openCreate = () => {
    selectedDepartment.value = null
    showForm.value = true
  }
  
  const openEdit = (department) => {
    selectedDepartment.value = department
    showForm.value = true
  }
  
  const closeForm = () => {
    showForm.value = false
    selectedDepartment.value = null
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
      await departementApi.delete(pendingDeleteId.value)
      showDeleteConfirm.value = false
      await fetchDepartments()
    } catch (err) {
      alert(err.response?.data?.detail || 'Gagal menghapus department')
    } finally {
      deleting.value = false
    }
  }

  onMounted(fetchDepartments)
  </script>