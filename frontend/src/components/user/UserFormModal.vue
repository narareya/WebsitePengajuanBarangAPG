<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="w-full max-w-md rounded-lg bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">{{ isEdit ? 'Edit User' : 'Tambah User' }}</h2>
  
        <div class="space-y-3">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Nama</label>
            <input v-model="form.name" type="text" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Email</label>
            <input v-model="form.email" type="email" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">
              Password {{ isEdit ? '(kosongkan jika tidak diubah)' : '' }}
            </label>
            <input v-model="form.password" type="password" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Role</label>
            <select v-model="form.role" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
              <option value="employee">Employee</option>
              <option value="manager">Manager</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Department</label>
            <select v-model.number="form.departement_id" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
              <option disabled value="">Pilih Department</option>
              <option v-for="d in departments" :key="d.departement_id" :value="d.departement_id">
                {{ d.departement_name }}
              </option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Status</label>
            <select v-model="form.user_status" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
              <option value="active">Active</option>
              <option value="off">Off</option>
            </select>
          </div>
        </div>
  
        <p v-if="formError" class="mt-3 text-sm text-red-500">{{ formError }}</p>
  
        <div class="mt-5 flex justify-end gap-2">
          <button @click="$emit('close')" class="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50">Batal</button>
          <button
            @click="handleSubmit"
            :disabled="submitting"
            class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-50"
          >
            {{ submitting ? 'Menyimpan...' : 'Simpan' }}
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import userApi from '@/api/userApi'
  import departementApi from '@/api/departementApi'
  
  const props = defineProps({
    user: { type: Object, default: null }
  })
  const emit = defineEmits(['close', 'saved'])
  
  const isEdit = computed(() => !!props.user)
  const submitting = ref(false)
  const formError = ref(null)
  const departments = ref([])
  
  const form = ref({
    name: props.user?.name || '',
    email: props.user?.email || '',
    password: '',
    role: props.user?.role || 'employee',
    departement_id: props.user?.departement_id || '',
    user_status: props.user?.user_status || 'active'
  })
  
  const fetchDepartments = async () => {
    const res = await departementApi.getAll()
    departments.value = res.data
  }
  
  const handleSubmit = async () => {
    formError.value = null
  
    if (!form.value.name || !form.value.email || !form.value.departement_id) {
      formError.value = 'Pastikan semua field wajib diisi'
      return
    }
    if (!isEdit.value && !form.value.password) {
      formError.value = 'Password wajib diisi untuk user baru'
      return
    }
  
    const payload = { ...form.value }
    if (isEdit.value && !payload.password) {
      delete payload.password
    }
  
    try {
      submitting.value = true
      if (isEdit.value) {
        await userApi.update(props.user.user_id, payload)
      } else {
        await userApi.create(payload)
      }
      emit('saved')
      emit('close')
    } catch (err) {
      formError.value = err.response?.data?.detail || 'Gagal menyimpan user'
    } finally {
      submitting.value = false
    }
  }
  
  onMounted(fetchDepartments)
  </script>