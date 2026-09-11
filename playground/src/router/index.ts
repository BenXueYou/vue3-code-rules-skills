import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated } from '../services/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !isAuthenticated())
    return {
      name: 'login',
      query: { redirect: to.fullPath },
    }

  if (to.name === 'login' && isAuthenticated())
    return { name: 'home' }

  return true
})

export default router
