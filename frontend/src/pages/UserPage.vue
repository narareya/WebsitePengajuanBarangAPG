<template>
    <div class="p-8">
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-50 text-indigo-600">
            <Users class="h-5 w-5" />
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Master User</h1>
            <p class="mt-0.5 text-sm text-gray-500">Kelola daftar user</p>
          </div>
        </div>
        <button @click="openCreate" class="flex items-center gap-1.5 rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
          <Plus class="h-4 w-4" />
          Tambah User
        </button>
      </div>
  
      <div class="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div class="relative w-full sm:max-w-xs">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari nama atau email..."
            class="w-full rounded-md border border-gray-300 py-2 pl-9 pr-3 text-sm focus:border-indigo-500 focus:outline-none"
          />
          <svg class="absolute left-3 top-2.5 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35M17 11a6 6 0 11-12 0 6 6 0 0112 0z" />
          </svg>
        </div>
  
        <div class="flex items-center gap-3">
          <select v-model="roleFilter" class="rounded-md border border-gray-300 py-2 px-3 text-sm focus:border-indigo-500 focus:outline-none">
            <option value="all">Semua Role</option>
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
            <option value="admin">Admin</option>
          </select>
          <select v-model="statusFilter" class="rounded-md border border-gray-300 py-2 px-3 text-sm focus:border-indigo-500 focus:outline-none">
            <option value="all">Semua Status</option>
            <option value="active">Aktif</option>
            <option value="inactive">Nonaktif</option>
          </select>
        </div>
      </div>
  
      <p v-if="loading" class="text-sm text-gray-500">Memuat data...</p>
      <p v-else-if="error" class="text-sm text-red-500">{{ error }}</p>
  
      <template v-else>
        <p v-if="filteredUsers.length === 0" class="rounded-md border border-gray-200 bg-white py-10 text-center text-sm text-gray-400">
          Tidak ada user yang cocok.
        </p>
  
        <UserTable v-else :users="paginatedUsers" @edit="openEdit" @delete="handleDelete" />
  
        <div v-if="filteredUsers.length > 0" class="mt-4 flex items-center justify-between">
          <p class="text-sm text-gray-500">
            Menampilkan {{ startIndex + 1 }}-{{ endIndex }} dari {{ filteredUsers.length }} user
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
  
      <UserFormModal
        v-if="showForm"
        :user="selectedUser"
        @close="closeForm"
        @saved="fetchUsers"
      />

      <ConfirmDialog
        v-if="showDeleteConfirm"
        title="Hapus user ini?"
        message="User yang dihapus tidak bisa dikembalikan."
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
  import { Users, Plus } from 'lucide-vue-next'
  import userApi from '@/api/userApi'
  import UserTable from '@/components/user/UserTable.vue'
  import UserFormModal from '@/components/user/UserFormModal.vue'
  import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
  
  const users = ref([])
  const loading = ref(true)
  const error = ref(null)
  const showForm = ref(false)
  const selectedUser = ref(null)
  
  const searchQuery = ref('')
  const roleFilter = ref('all')
  const statusFilter = ref('all')
  const currentPage = ref(1)
  const pageSize = 10
  
  const fetchUsers = async () => {
    try {
      loading.value = true
      const res = await userApi.getAll()
      users.value = res.data
    } catch (err) {
      console.error(err)
      error.value = 'Gagal memuat data user'
    } finally {
      loading.value = false
    }
  }
  
  const filteredUsers = computed(() => {
    let result = users.value
  
    if (roleFilter.value !== 'all') {
      result = result.filter((u) => u.role === roleFilter.value)
    }
    if (statusFilter.value !== 'all') {
      result = result.filter((u) => u.user_status === statusFilter.value)
    }
  
    const q = searchQuery.value.trim().toLowerCase()
    if (q) {
      result = result.filter(
        (u) => u.name?.toLowerCase().includes(q) || u.email?.toLowerCase().includes(q)
      )
    }
  
    return result
  })
  
  const totalPages = computed(() => Math.max(1, Math.ceil(filteredUsers.value.length / pageSize)))
  const startIndex = computed(() => (currentPage.value - 1) * pageSize)
  const endIndex = computed(() => Math.min(startIndex.value + pageSize, filteredUsers.value.length))
  const paginatedUsers = computed(() => filteredUsers.value.slice(startIndex.value, startIndex.value + pageSize))
  
  watch([searchQuery, roleFilter, statusFilter], () => {
    currentPage.value = 1
  })
  watch(totalPages, (newTotal) => {
    if (currentPage.value > newTotal) currentPage.value = newTotal
  })
  
  const openCreate = () => {
    selectedUser.value = null
    showForm.value = true
  }
  
  const openEdit = (user) => {
    selectedUser.value = user
    showForm.value = true
  }
  
  const closeForm = () => {
    showForm.value = false
    selectedUser.value = null
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
      await userApi.delete(pendingDeleteId.value)
      showDeleteConfirm.value = false
      await fetchUsers()
    } catch (err) {
      alert(err.response?.data?.detail || 'Gagal menghapus user')
    } finally {
      deleting.value = false
    }
  }

  onMounted(fetchUsers)
  </script>