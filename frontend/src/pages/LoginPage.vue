<template>
  <div class="min-h-screen flex bg-white">
    <div class="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-20 py-12">
      <div class="w-full max-w-sm mx-auto lg:mx-0">
        <BrandLogo class="mb-10 mx-auto" />
        <h2 class="text-2xl font-bold text-gray-900">Sign in to your account</h2>
        <LoginForm class="mt-8" @submit="handleLogin" />
        <p v-if="errorMsg" class="text-red-500 text-sm mt-4">{{ errorMsg }}</p>
      </div>
    </div>
    <AuthHeroImage />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BrandLogo from '@/components/login/BrandLogo.vue'
import LoginForm from '@/components/login/LoginForm.vue'
import AuthHeroImage from '@/components/login/AuthHeroImage.vue'
import api from '@/api/axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const errorMsg = ref('')

async function handleLogin(credentials) {
  errorMsg.value = ''
  try {
    const res = await api.post('auth/login', {
      email: credentials.email,
      password: credentials.password,
    })

    authStore.setAuth(res.data.access_token, res.data.user)
    router.push('/dashboard')
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Login gagal, cek email dan password Anda.'
  }
}
</script>