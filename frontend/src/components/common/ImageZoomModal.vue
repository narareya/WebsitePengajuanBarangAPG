<template>
  <div class="fixed inset-0 z-[70] flex items-center justify-center bg-black/80 p-4" @click.self="$emit('close')">
    <button
      @click="$emit('close')"
      class="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20"
    >
      <X class="h-5 w-5" />
    </button>

    <div v-if="loading" class="flex items-center gap-2 text-sm text-white/80">
      <span class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
      Memuat gambar...
    </div>
    <p v-else-if="error" class="text-sm text-white/80">{{ error }}</p>
    <img v-else :src="imageUrl" :alt="filename" class="max-h-[90vh] max-w-[90vw] rounded-lg object-contain" />

    <p v-if="filename && !loading && !error" class="absolute bottom-4 left-1/2 -translate-x-1/2 text-xs text-white/60">
      {{ filename }}
    </p>
  </div>
</template>

<script setup>
import { X } from 'lucide-vue-next'

defineProps({
  imageUrl: { type: String, default: null },
  filename: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  error: { type: String, default: null },
})
defineEmits(['close'])
</script>
