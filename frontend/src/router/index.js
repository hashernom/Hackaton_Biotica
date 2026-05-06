import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView    from '../views/HomeView.vue'
import ChatView    from '../views/ChatView.vue'
import LoginView   from '../views/LoginView.vue'
import AdminView   from '../views/AdminView.vue'

const routes = [
  { path: '/',      name: 'home',  component: HomeView,  meta: { title: 'Biótica – Inicio' } },
  { path: '/chat',  name: 'chat',  component: ChatView,  meta: { title: 'Biótica – Asistente' } },
  { path: '/login', name: 'login', component: LoginView, meta: { title: 'Admin – Login' } },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView,
    meta: { title: 'Panel de Control', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() { return { top: 0 } }
})

// Guard: redirige al login si no está autenticado
router.beforeEach((to, _from, next) => {
  document.title = to.meta.title || 'Biótica Consultores'
  if (to.meta.requiresAuth && !store.getters.isAdminLoggedIn) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router