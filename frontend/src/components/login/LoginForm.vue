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
  
      <AppButton type="submit" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign in' }}
      </AppButton>
    </form>
  </template>

  <script setup>
  import { reactive } from 'vue'
  import InputField from '@/components/common/InputField.vue'
  import AppButton from '@/components/common/AppButton.vue'

  defineProps({
    loading: { type: Boolean, default: false },
  })
  const emit = defineEmits(['submit'])
  
  const form = reactive({
    email: '',
    password: '',
    rememberMe: false,
  })
  
  function handleSubmit() {
    emit('submit', { ...form })
  }

  function setCredentials(email, password) {
    form.email = email
    form.password = password
  }

  defineExpose({ setCredentials })
  </script>