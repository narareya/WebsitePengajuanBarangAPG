<template>
    <button
      :type="type"
      class="flex w-full items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-semibold shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
      :class="variantClasses"
      :disabled="disabled"
    >
      <slot name="icon" />
      <slot />
    </button>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  
  const props = defineProps({
    type: {
      type: String,
      default: 'button',
    },
    variant: {
      type: String,
      default: 'primary', // 'primary' | 'outline'
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  })
  
  const variantClasses = computed(() => {
    if (props.variant === 'outline') {
      return 'border border-gray-300 text-gray-900 hover:bg-gray-50 focus:ring-indigo-500'
    }
    return 'bg-indigo-600 text-white hover:bg-indigo-500 focus:ring-indigo-500'
  })
  </script>