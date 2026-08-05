<template>
    <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Kode</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Nama</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Harga</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Status</th>
            <th class="px-4 py-3 text-right text-xs font-semibold uppercase text-gray-500">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="products.length === 0">
            <td colspan="5" class="px-4 py-6 text-center text-sm text-gray-400">Belum ada produk</td>
          </tr>
          <tr v-for="p in products" :key="p.product_id">
            <td class="px-4 py-3 text-sm text-gray-700">{{ p.product_code }}</td>
            <td class="px-4 py-3 text-sm text-gray-700">{{ p.product_name }}</td>
            <td class="px-4 py-3 text-sm text-gray-700">{{ formatPrice(p.product_price) }}</td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-1 text-xs font-medium"
                :class="p.product_status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
              >
                {{ p.product_status }}
              </span>
            </td>
            <td class="px-4 py-3 text-right">
              <button @click="$emit('edit', p)" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">Edit</button>
              <button @click="$emit('delete', p.product_id)" class="ml-3 text-sm font-medium text-red-500 hover:text-red-400">Hapus</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({ products: { type: Array, required: true } })
  defineEmits(['edit', 'delete'])
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price)
  }
  </script>