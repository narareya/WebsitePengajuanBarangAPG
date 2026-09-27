<template>
  <div class="pointer-events-none fixed bottom-4 right-4 z-[100] flex w-full max-w-sm flex-col gap-2">
    <TransitionGroup
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-start gap-2.5 rounded-lg border bg-white p-3 shadow-lg"
        :class="toast.type === 'success' ? 'border-green-200' : 'border-red-200'"
      >
        <component
          :is="toast.type === 'success' ? CheckCircle2 : AlertCircle"
          class="mt-0.5 h-4 w-4 shrink-0"
          :class="toast.type === 'success' ? 'text-green-600' : 'text-red-600'"
        />
        <p class="flex-1 text-sm text-gray-700">{{ toast.message }}</p>
        <button @click="toastStore.dismiss(toast.id)" class="shrink-0 text-gray-400 hover:text-gray-600">
          <X class="h-4 w-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { AlertCircle, CheckCircle2, X } from 'lucide-vue-next'
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()
</script>
