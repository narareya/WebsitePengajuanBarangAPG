<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="w-full max-w-md rounded-lg bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">{{ isEdit ? 'Edit Produk' : 'Tambah Produk' }}</h2>
  
        <div class="space-y-3">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Kode Produk</label>
            <input v-model="form.product_code" type="text" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Nama Produk</label>
            <input v-model="form.product_name" type="text" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Deskripsi</label>
            <textarea v-model="form.product_desc" rows="2" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"></textarea>
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Harga</label>
            <input v-model.number="form.product_price" type="number" min="0" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm" />
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Status</label>
            <select v-model="form.product_status" class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm">
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
  import productApi from '@/api/productApi'
  
  const props = defineProps({
    product: { type: Object, default: null }
  })
  const emit = defineEmits(['close', 'saved'])
  
  const isEdit = computed(() => !!props.product)
  const submitting = ref(false)
  const formError = ref(null)
  
  const form = ref({
    product_code: props.product?.product_code || '',
    product_name: props.product?.product_name || '',
    product_desc: props.product?.product_desc || '',
    product_price: props.product?.product_price || 0,
    product_status: props.product?.product_status || 'active'
  })
  
  const handleSubmit = async () => {
    formError.value = null
    if (!form.value.product_code || !form.value.product_name || form.value.product_price <= 0) {
      formError.value = 'Pastikan semua field wajib diisi dengan benar'
      return
    }
  
    try {
      submitting.value = true
      if (isEdit.value) {
        await productApi.update(props.product.product_id, form.value)
      } else {
        await productApi.create(form.value)
      }
      emit('saved')
      emit('close')
    } catch (err) {
      formError.value = err.response?.data?.detail || 'Gagal menyimpan produk'
    } finally {
      submitting.value = false
    }
  }
  </script>