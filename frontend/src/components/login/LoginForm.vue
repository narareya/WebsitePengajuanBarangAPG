<template>
    <form class="space-y-6" @submit.prevent="handleSubmit">
      <InputField
        id="email"
        v-model="form.email"
        label="Email address"
        type="email"
        autocomplete="email"
        required
      />
  
      <InputField
        id="password"
        v-model="form.password"
        label="Password"
        type="password"
        autocomplete="current-password"
        required
      />
  
      <AppButton type="submit">Sign in</AppButton>
    </form>
  </template>
  
  <script setup>
  import { reactive } from 'vue'
  import InputField from '@/components/common/InputField.vue'
  import AppButton from '@/components/common/AppButton.vue'
  
  const emit = defineEmits(['submit'])
  
  const form = reactive({
    email: '',
    password: '',
    rememberMe: false,
  })
  
  function handleSubmit() {
    emit('submit', { ...form })
  }
  </script>