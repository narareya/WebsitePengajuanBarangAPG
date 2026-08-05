<template>
    <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Kode</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Nama</th>
            <th class="px-4 py-3 text-left text-xs font-semibold uppercase text-gray-500">Status</th>
            <th class="px-4 py-3 text-right text-xs font-semibold uppercase text-gray-500">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="departments.length === 0">
            <td colspan="4" class="px-4 py-6 text-center text-sm text-gray-400">Belum ada department</td>
          </tr>
          <tr v-for="d in departments" :key="d.departement_id">
            <td class="px-4 py-3 text-sm text-gray-700">{{ d.departement_code }}</td>
            <td class="px-4 py-3 text-sm text-gray-700">{{ d.departement_name }}</td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-1 text-xs font-medium"
                :class="d.departement_status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'"
              >
                {{ d.departement_status }}
              </span>
            </td>
            <td class="px-4 py-3 text-right">
              <button @click="$emit('edit', d)" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">Edit</button>
              <button @click="$emit('delete', d.departement_id)" class="ml-3 text-sm font-medium text-red-500 hover:text-red-400">Hapus</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script setup>
  defineProps({ departments: { type: Array, required: true } })
  defineEmits(['edit', 'delete'])
  </script>