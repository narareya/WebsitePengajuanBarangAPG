<template>
    <div class="rounded-lg border border-gray-200 bg-white p-5 transition-shadow hover:shadow-sm">
      <div class="flex items-start justify-between">
        <div class="min-w-0">
          <p class="text-sm font-medium text-gray-500">{{ label }}</p>
  
          <div v-if="value === null" class="mt-2 h-6 w-16 animate-pulse rounded bg-gray-100"></div>
          <p v-else class="mt-1 text-2xl font-semibold text-gray-900" :class="{ capitalize }">
            {{ value }}
          </p>
        </div>
  
        <div class="rounded-lg p-2.5" :class="iconWrapClass">
          <component :is="iconComponent" class="h-5 w-5" :class="iconClass" />
        </div>
      </div>

    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { User, FileText, Clock } from 'lucide-vue-next'
  
  const props = defineProps({
    label: String,
    value: [String, Number, null],
    icon: String,
    variant: { type: String, default: 'neutral' },
    trend: { type: [Number, null], default: null },
    capitalize: { type: Boolean, default: false },
  })
  
  const icons = { user: User, 'file-text': FileText, clock: Clock }
  const iconComponent = computed(() => icons[props.icon] || FileText)
  
  const variants = {
    neutral: { wrap: 'bg-gray-100', icon: 'text-gray-600' },
    blue: { wrap: 'bg-blue-50', icon: 'text-blue-600' },
    amber: { wrap: 'bg-amber-50', icon: 'text-amber-600' },
  }
  const iconWrapClass = computed(() => variants[props.variant]?.wrap || variants.neutral.wrap)
  const iconClass = computed(() => variants[props.variant]?.icon || variants.neutral.icon)
  </script>