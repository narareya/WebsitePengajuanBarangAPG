<template>
  <div class="p-8">
    <div class="mb-8 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p class="mt-1 text-sm text-gray-500">
          Selamat datang,
          <span class="font-medium text-gray-700">{{ authStore.user?.name }}</span>
        </p>
      </div>
      <div class="text-sm text-gray-400">
        {{ todayLabel }}
      </div>
    </div>

    <div
      v-if="error"
      class="mb-6 flex items-center justify-between rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
    >
      <span>Gagal memuat data dashboard: {{ error }}</span>
      <button @click="fetchSummary" class="font-medium underline hover:text-red-800">
        Coba lagi
      </button>
    </div>

    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <StatCard
        label="Role Kamu"
        :value="authStore.role"
        icon="user"
        variant="neutral"
        capitalize
      />

      <StatCard
        label="Total Pengajuan"
        :value="loading ? null : summary.totalSubmissions"
        icon="file-text"
        variant="blue"
        :trend="summary.totalTrend"
      />

      <StatCard
        label="Menunggu Approval"
        :value="loading ? null : summary.pendingApproval"
        icon="clock"
        variant="amber"
      />
    </div>

    <div class="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-3">
      <div class="rounded-lg border border-gray-200 bg-white p-5 lg:col-span-1">
        <p class="text-sm font-medium text-gray-500">Status Pengajuan</p>

        <div v-if="loading" class="mt-4 space-y-3">
          <div v-for="i in 3" :key="i" class="h-4 w-full animate-pulse rounded bg-gray-100"></div>
        </div>

        <div v-else class="mt-4 space-y-3">
          <div
            v-for="item in statusBreakdown"
            :key="item.label"
            class="flex items-center justify-between text-sm"
          >
            <div class="flex items-center gap-2">
              <span class="h-2.5 w-2.5 rounded-full" :class="item.dotClass"></span>
              <span class="text-gray-600">{{ item.label }}</span>
            </div>
            <span class="font-semibold text-gray-900">{{ item.value }}</span>
          </div>
        </div>
      </div>

      <div class="rounded-lg border border-gray-200 bg-white p-5 lg:col-span-2">
        <p class="text-sm font-medium text-gray-500">Aktivitas Terbaru</p>

        <div v-if="loading" class="mt-4 space-y-4">
          <div v-for="i in 4" :key="i" class="flex items-center gap-3">
            <div class="h-8 w-8 animate-pulse rounded-full bg-gray-100"></div>
            <div class="h-4 flex-1 animate-pulse rounded bg-gray-100"></div>
          </div>
        </div>

        <ul v-else-if="recentActivity.length" class="mt-4 divide-y divide-gray-100">
          <li
            v-for="item in recentActivity"
            :key="item.id"
            class="flex items-center gap-3 py-3 first:pt-0 last:pb-0"
          >
            <span
              class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold"
              :class="statusBadgeClass(item.status)"
            >
              {{ item.statusLabel?.[0]?.toUpperCase() }}
            </span>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-medium text-gray-900">{{ item.title }}</p>
              <p class="text-xs text-gray-500">
                {{ item.actor }} · {{ formatRelativeTime(item.createdAt) }}
              </p>
            </div>
            <span
              class="shrink-0 rounded-full px-2 py-0.5 text-xs font-medium"
              :class="statusBadgeClass(item.status)"
            >
              {{ item.statusLabel }}
            </span>
          </li>
        </ul>

        <p v-else class="mt-4 text-sm text-gray-400">Belum ada aktivitas.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import StatCard from '@/components/dashboard/StatCard.vue'

const authStore = useAuthStore()

const loading = ref(true)
const error = ref(null)
const summary = ref({
  totalSubmissions: 0,
  pendingApproval: 0,
  totalTrend: null,
  byStatus: {},
})
const recentActivity = ref([])

const todayLabel = computed(() =>
  new Date().toLocaleDateString('id-ID', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }),
)

const statusDotMap = {
  approved: 'bg-green-500',
  pending: 'bg-amber-500',
  rejected: 'bg-red-500',
  draft: 'bg-gray-400',
}

const statusBreakdown = computed(() =>
  Object.entries(summary.value.byStatus || {}).map(([key, value]) => ({
    label: key.charAt(0).toUpperCase() + key.slice(1),
    value,
    dotClass: statusDotMap[key] || 'bg-gray-400',
  })),
)

function statusBadgeClass(status) {
  const map = {
    approved: 'bg-green-100 text-green-700',
    pending: 'bg-amber-100 text-amber-700',
    rejected: 'bg-red-100 text-red-700',
    draft: 'bg-gray-100 text-gray-600',
  }
  return map[status] || 'bg-gray-100 text-gray-600'
}

function formatRelativeTime(dateStr) {
  if (!dateStr) return ''
  const diffMs = Date.now() - new Date(dateStr).getTime()
  const minutes = Math.floor(diffMs / 60000)
  if (minutes < 1) return 'baru saja'
  if (minutes < 60) return `${minutes} menit lalu`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} jam lalu`
  const days = Math.floor(hours / 24)
  return `${days} hari lalu`
}

async function fetchSummary() {
  loading.value = true
  error.value = null
  try {
    const [summaryRes, activityRes] = await Promise.all([
      api.get('/dashboard/summary'),
      api.get('/dashboard/recent-activity', { params: { limit: 5 } }),
    ])

    const s = summaryRes.data
    summary.value = {
      totalSubmissions: s.total_submissions,
      pendingApproval: s.pending_approval,
      totalTrend: s.total_trend,
      byStatus: s.by_status,
    }

    recentActivity.value = activityRes.data.map((item) => ({
      id: item.id,
      title: item.title,
      actor: item.actor,
      status: item.status,
      statusLabel: item.status_label,
      createdAt: item.created_at,
    }))
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Terjadi kesalahan'
  } finally {
    loading.value = false
  }
}

onMounted(fetchSummary)
</script>
