<template>
  <div class="min-h-screen flex bg-white">
    <div class="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-20 py-12">
      <div class="w-full max-w-sm mx-auto lg:mx-0">
        <BrandLogo class="mb-10 mx-auto" />
        <h2 class="text-2xl font-bold text-gray-900">Sign in to your account</h2>
        <LoginForm ref="loginFormRef" class="mt-8" :loading="loading" @submit="handleLogin" />
        <p v-if="errorMsg" class="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-600">{{ errorMsg }}</p>

        <div class="mt-6 rounded-lg border border-gray-200 bg-gray-50 p-4">
          <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Akun Demo</p>
          <div class="mt-2 space-y-1.5">
            <button
              v-for="demo in demoAccounts"
              :key="demo.email"
              type="button"
              @click="fillDemo(demo)"
              class="flex w-full items-center justify-between rounded-md px-2 py-1.5 text-left text-xs hover:bg-gray-100"
            >
              <span class="font-medium text-gray-700">{{ demo.role }}</span>
              <span class="text-gray-400">{{ demo.email }} / {{ demo.password }}</span>
            </button>
          </div>
        </div>
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
const loading = ref(false)
const loginFormRef = ref(null)

const demoAccounts = [
  { role: 'Admin', email: 'admin@apg.com', password: 'admin123' },
  { role: 'Manager', email: 'budi@apg.com', password: 'budi123' },
  { role: 'Employee', email: 'siti@apg.com', password: 'siti123' },
]

function fillDemo(demo) {
  loginFormRef.value?.setCredentials(demo.email, demo.password)
}

async function handleLogin(credentials) {
  errorMsg.value = ''
  loading.value = true
  try {
    const res = await api.post('auth/login', {
      email: credentials.email,
      password: credentials.password,
    })

    authStore.setAuth(res.data.access_token, res.data.user)
    router.push('/dashboard')
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Login gagal, cek email dan password Anda.'
  } finally {
    loading.value = false
  }
}
</script>