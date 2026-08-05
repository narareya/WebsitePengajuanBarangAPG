<template>
  <aside class="flex h-screen w-64 flex-col border-r border-gray-200 bg-white">
    <div class="flex items-center justify-center px-6 pt-6 pb-4">
      <img :src="logo" alt="Amazink People Group" class="h-20 w-auto" />
    </div>
    <nav class="flex-1 overflow-y-auto px-4">
      <ul class="space-y-1">
        <li v-for="item in visibleMenus" :key="item.path">
          <router-link
            :to="item.path"
            class="group flex items-center justify-between rounded-md px-3 py-2 text-sm font-semibold transition-colors"
            :class="isActive(item.path)
              ? 'bg-gray-100 text-indigo-600'
              : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'"
          >
            <span class="flex items-center gap-3">
              <component
                :is="item.iconComponent"
                class="h-5 w-5 shrink-0"
                :class="isActive(item.path) ? 'text-indigo-600' : 'text-gray-400 group-hover:text-gray-600'"
              />
              {{ item.label }}
            </span>
          </router-link>
        </li>
      </ul>
    </nav>

    <div ref="profileRef" class="relative border-t border-gray-100 px-4 py-4">
      <div
        v-if="showMenu"
        class="absolute bottom-full left-4 right-4 mb-2 overflow-hidden rounded-md border border-gray-200 bg-white shadow-lg"
      >
        <button
          @click="handleLogout"
          class="flex w-full items-center gap-2 px-3 py-2.5 text-left text-sm font-medium text-red-600 hover:bg-red-50"
        >
          <LogOut class="h-4 w-4" />
          Logout
        </button>
      </div>

      <button
        type="button"
        class="flex w-full items-center gap-3 rounded-md px-2 py-1.5 hover:bg-gray-50"
        @click="showMenu = !showMenu"
      >
        <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-sm font-semibold text-indigo-600">
          {{ initials }}
        </div>
        <div class="flex flex-1 flex-col text-left">
          <span class="text-sm font-semibold text-gray-900">{{ authStore.user?.name }}</span>
          <span class="text-xs text-gray-400 capitalize">{{ authStore.role }}</span>
        </div>
        <ChevronUp
          class="h-4 w-4 shrink-0 text-gray-400 transition-transform"
          :class="{ 'rotate-180': showMenu }"
        />
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LogOut, ChevronUp } from 'lucide-vue-next'
import { sidebarMenus } from '@/config/SidebarNav'
import { iconMap } from '@/config/Icons'
import { useAuthStore } from '@/stores/auth'
import logo from '@/assets/logoamazink.png'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const showMenu = ref(false)
const profileRef = ref(null)

const visibleMenus = computed(() =>
  sidebarMenus
    .filter(menu => menu.roles.includes(authStore.role))
    .map(menu => ({ ...menu, iconComponent: iconMap[menu.icon] }))
)

const isActive = (path) => route.path.startsWith(path)

const initials = computed(() => {
  const name = authStore.user?.name || ''
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
})

const handleLogout = () => {
  showMenu.value = false
  authStore.logout()
  router.push('/login')
}

const handleClickOutside = (event) => {
  if (profileRef.value && !profileRef.value.contains(event.target)) {
    showMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>