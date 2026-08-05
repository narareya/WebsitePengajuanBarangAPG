<template>
    <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="w-full max-w-lg rounded-lg bg-white p-6">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">
          {{ isEdit ? 'Edit Pengajuan' : 'Buat Pengajuan Baru' }}
        </h2>
  
        <div v-for="(item, index) in form.items" :key="index" class="mb-3 flex items-center gap-2">
          <select v-model="item.product_id" class="flex-1 rounded-md border border-gray-300 px-3 py-2 text-sm">
            <option disabled value="">Pilih Produk</option>
            <option v-for="p in products" :key="p.product_id" :value="p.product_id">
              {{ p.product_name }}
            </option>
          </select>
          <input
            v-model.number="item.quantity"
            type="number"
            min="1"
            placeholder="Qty"
            class="w-20 rounded-md border border-gray-300 px-3 py-2 text-sm"
          />
          <button v-if="form.items.length > 1" @click="removeItem(index)" class="text-red-400 hover:text-red-500" type="button">
            ✕
          </button>
        </div>
  
        <button @click="addItem" type="button" class="mb-4 text-sm font-medium text-indigo-600 hover:text-indigo-500">
          + Tambah Barang
        </button>

        <div class="mb-4">
          <label class="mb-1 block text-sm font-medium text-gray-700">Lampiran (opsional)</label>
          <div v-if="previewUrl" class="mb-2 overflow-hidden rounded-md border border-gray-200">
            <img :src="previewUrl" alt="Preview lampiran" class="max-h-40 w-full object-contain" />
          </div>
          <input
            type="file"
            accept="image/*"
            @change="handleFileChange"
            class="block w-full text-xs text-gray-500 file:mr-3 file:rounded-md file:border-0 file:bg-indigo-50 file:px-3 file:py-1.5 file:text-xs file:font-medium file:text-indigo-600 hover:file:bg-indigo-100"
          />
        </div>

        <p v-if="formError" class="mb-3 text-sm text-red-500">{{ formError }}</p>
  
        <div class="flex justify-end gap-2">
          <button @click="$emit('close')" type="button" class="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50">
            Batal
          </button>
          <button
            @click="handleSubmit"
            type="button"
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
  import { ref, computed, onBeforeUnmount } from 'vue'
  import requestApi from '@/api/requestApi'

  const props = defineProps({
    products: { type: Array, required: true },
    requestData: { type: Object, default: null }  // kalau ada, berarti mode edit
  })
  const emit = defineEmits(['close', 'submitted'])

  const isEdit = computed(() => !!props.requestData)
  const submitting = ref(false)
  const formError = ref(null)
  const selectedFile = ref(null)
  const previewUrl = ref(null)

  const form = ref({
    items: props.requestData?.details?.map(d => ({
      product_id: d.product_id,
      quantity: d.quantity
    })) || [{ product_id: '', quantity: 1 }]
  })

  const addItem = () => form.value.items.push({ product_id: '', quantity: 1 })
  const removeItem = (index) => form.value.items.splice(index, 1)

  const handleFileChange = (e) => {
    if (previewUrl.value) window.URL.revokeObjectURL(previewUrl.value)
    selectedFile.value = e.target.files?.[0] || null
    previewUrl.value = selectedFile.value ? window.URL.createObjectURL(selectedFile.value) : null
  }

  const handleSubmit = async () => {
    formError.value = null
    const invalid = form.value.items.some(i => !i.product_id || !i.quantity || i.quantity < 1)
    if (invalid) {
      formError.value = 'Pastikan semua barang & jumlah sudah diisi dengan benar'
      return
    }

    try {
      submitting.value = true
      let requestId
      if (isEdit.value) {
        requestId = props.requestData.request_id
        await requestApi.updateItems(requestId, { items: form.value.items })
      } else {
        const res = await requestApi.create({ items: form.value.items })
        requestId = res.data.request_id
      }
      if (selectedFile.value) {
        await requestApi.uploadAttachment(requestId, selectedFile.value)
      }
      emit('submitted')
      emit('close')
    } catch (err) {
      formError.value = err.response?.data?.detail || 'Gagal menyimpan pengajuan'
    } finally {
      submitting.value = false
    }
  }

  onBeforeUnmount(() => {
    if (previewUrl.value) window.URL.revokeObjectURL(previewUrl.value)
  })
  </script>