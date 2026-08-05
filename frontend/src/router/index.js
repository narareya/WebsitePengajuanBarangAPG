import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginPage from '@/pages/LoginPage.vue'
import MainLayout from '@/components/layout/MainLayout.vue'
import DashboardPage from '@/pages/DashboardPage.vue'
import RequestPage from '@/pages/RequestPage.vue'
import ProductPage from '@/pages/ProductPage.vue'
import DepartementPage from '@/pages/DepartementPage.vue'
import UserPage from '@/pages/UserPage.vue'
import ActivityLogPage from '@/pages/master/ActivityLogPage.vue'

const routes = [
  {
    path: '/login',
    component: LoginPage
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      { path: 'dashboard', component: DashboardPage, meta: { roles: ['employee', 'manager', 'admin'] } },
      { path: 'pengajuan', component: RequestPage, meta: { roles: ['employee', 'manager', 'admin'] } },
      { path: 'master/products', component: ProductPage, meta: { roles: ['admin'] } },
      { path: 'master/departments', component: DepartementPage, meta: { roles: ['admin'] } },
      { path: 'master/users', component: UserPage, meta: { roles: ['admin'] } },
      { path: 'activity-log', component: ActivityLogPage, meta: { roles: ['admin'] } },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return '/login'
  }

  if (to.meta.roles && !to.meta.roles.includes(authStore.role)) {
    return '/dashboard'
  }

  return true
})

export default router