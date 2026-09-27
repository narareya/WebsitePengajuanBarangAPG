<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
    <div class="w-full max-w-sm rounded-lg bg-white p-6">
      <h2 class="text-lg font-semibold text-gray-900">Tambah Stok</h2>
      <p class="mt-1 text-sm text-gray-500">
        {{ product.product_name }} — stok saat ini: <span class="font-medium text-gray-700">{{ product.stock_quantity }}</span>
      </p>

      <label class="mb-1 mt-4 block text-sm font-medium text-gray-700">Jumlah tambahan</label>
      <input
        v-model.number="quantity"
        type="number"
        min="1"
        autofocus
        class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none"
        placeholder="mis. 20"
      />
      <p v-if="quantity > 0" class="mt-1 text-xs text-gray-400">
        Stok jadi: {{ product.stock_quantity + quantity }}
      </p>

      <p v-if="formError" class="mt-3 text-sm text-red-500">{{ formError }}</p>

      <div class="mt-5 flex justify-end gap-2">
        <button @click="$emit('close')" type="button" class="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50">
          Batal
        </button>
        <button
          @click="handleSubmit"
          type="button"
          :disabled="submitting || !quantity || quantity <= 0"
          class="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-50"
        >
          {{ submitting ? 'Menyimpan...' : 'Tambah Stok' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import productApi from '@/api/productApi'

const props = defineProps({
  product: { type: Object, required: true }
})
const emit = defineEmits(['close', 'saved'])

const quantity = ref(null)
const submitting = ref(false)
const formError = ref(null)

const handleSubmit = async () => {
  formError.value = null
  try {
    submitting.value = true
    await productApi.addStock(props.product.product_id, quantity.value)
    emit('saved')
    emit('close')
  } catch (err) {
    formError.value = err.response?.data?.detail || 'Gagal menambah stok'
  } finally {
    submitting.value = false
  }
}
</script>
