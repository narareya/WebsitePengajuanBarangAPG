<template>
    <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Kode</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Nama</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Harga</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Stok</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Status</th>
            <th class="px-4 py-3 text-right text-xs font-semibold uppercase text-gray-500">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="products.length === 0">
            <td colspan="6" class="px-4 py-6 text-center text-sm text-gray-400">Belum ada produk</td>
          </tr>
          <tr v-for="p in products" :key="p.product_id">
            <td class="px-4 py-3 text-sm text-gray-700">{{ p.product_code }}</td>
            <td class="px-4 py-3 text-sm text-gray-700">{{ p.product_name }}</td>
            <td class="px-4 py-3 text-sm text-gray-700">{{ formatPrice(p.product_price) }}</td>
            <td class="px-4 py-3 text-sm">
              <span
                class="font-medium"
                :class="p.stock_quantity <= 0 ? 'text-red-600' : p.stock_quantity <= 5 ? 'text-amber-600' : 'text-gray-700'"
              >
                {{ p.stock_quantity }}
              </span>
              <span
                v-if="p.stock_quantity <= 5"
                class="ml-1.5 rounded-full px-1.5 py-0.5 text-[10px] font-medium"
                :class="p.stock_quantity <= 0 ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'"
              >
                {{ p.stock_quantity <= 0 ? 'Habis' : 'Menipis' }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-1 text-xs font-medium"
                :class="p.product_status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
              >
                {{ p.product_status }}
              </span>
            </td>
            <td class="px-4 py-3 text-right">
              <button
                @click="$emit('add-stock', p)"
                class="inline-flex items-center gap-1 rounded-md bg-indigo-50 px-2.5 py-1 text-sm font-medium text-indigo-700 hover:bg-indigo-100"
              >
                <Plus class="h-3.5 w-3.5" />
                Stok
              </button>
              <button @click="$emit('edit', p)" class="ml-3 text-sm font-medium text-indigo-600 hover:text-indigo-500">Edit</button>
              <button @click="$emit('delete', p.product_id)" class="ml-3 text-sm font-medium text-red-500 hover:text-red-400">Hapus</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script setup>
  import { Plus } from 'lucide-vue-next'

  defineProps({ products: { type: Array, required: true } })
  defineEmits(['edit', 'delete', 'add-stock'])

  const formatPrice = (price) => {
    return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price)
  }
  </script>
