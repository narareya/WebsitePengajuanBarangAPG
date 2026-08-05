<template>
    <div class="hidden lg:block relative w-1/2">
      <img :src="src" :alt="alt" class="absolute inset-0 h-full w-full object-cover" />
    </div>
  </template>
  
  <script setup>
  defineProps({
    src: {
      type: String,
      default: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1400&q=80',
    },
    alt: {
      type: String,
      default: 'Desk setup',
    },
  })
  </script>