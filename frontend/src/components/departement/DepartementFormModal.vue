<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="w-full max-w-md rounded-lg bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">{{ isEdit ? 'Edit Department' : 'Tambah Department' }}</h2>
  
        <div class="space-y-3">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Kode Department</label>
            <input v-model="form.departement_code" type="text" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Nama Department</label>
            <input v-model="form.departement_name" type="text" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Status</label>
            <select v-model="form.departement_status" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
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
  import { ref, computed } from 'vue'
  import departementApi from '@/api/departementApi'
  
  const props = defineProps({
    department: { type: Object, default: null }
  })
  const emit = defineEmits(['close', 'saved'])
  
  const isEdit = computed(() => !!props.department)
  const submitting = ref(false)
  const formError = ref(null)
  
  const form = ref({
    departement_code: props.department?.departement_code || '',
    departement_name: props.department?.departement_name || '',
    departement_status: props.department?.departement_status || 'active'
  })
  
  const handleSubmit = async () => {
    formError.value = null
    if (!form.value.departement_code || !form.value.departement_name) {
      formError.value = 'Pastikan semua field wajib diisi'
      return
    }
  
    try {
      submitting.value = true
      if (isEdit.value) {
        await departementApi.update(props.department.departement_id, form.value)
      } else {
        await departementApi.create(form.value)
      }
      emit('saved')
      emit('close')
    } catch (err) {
      formError.value = err.response?.data?.detail || 'Gagal menyimpan department'
    } finally {
      submitting.value = false
    }
  }
  </script>