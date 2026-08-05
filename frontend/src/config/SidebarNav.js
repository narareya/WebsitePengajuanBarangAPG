export const sidebarMenus = [
  {
    label: 'Dashboard',
    path: '/dashboard',
    icon: 'home',
    roles: ['employee', 'manager', 'admin']
  },
  {
    label: 'Pengajuan',
    path: '/pengajuan',
    icon: 'document',
    roles: ['employee', 'manager', 'admin']
  },
  {
    label: 'Users',
    path: '/master/users',
    icon: 'users',
    roles: ['admin']
  },
  {
    label: 'Departments',
    path: '/master/departments',
    icon: 'folder',
    roles: ['admin']
  },
  {
    label: 'Products',
    path: '/master/products',
    icon: 'box',
    roles: ['admin']
  }
]