import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    {
      path: "/",
      component: () => import("@/layouts/PublicLayout.vue"),
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import("@/components/inicio/Login.vue")
        },
        {
          path: 'register',
          name: 'register',
          component: () => import("@/components/inicio/Register.vue")
        },
        {
          path: '',
          redirect: { name: 'login' }
        }
      ],
    },
    {
      path: "/inicio",
      name: 'inicio',
      component: () => import("@/layouts/UsuarioLayout.vue"),
      meta: { requiresAuth: true },
      children: [
        {
          path: '/inicio/productos',
          name: 'productos',
          component: () => import("@/components/productos/AllProducts.vue"),
          meta: { requiresAuth: true }
        },
        {
          path: '/inicio/ventas',
          name: 'ventas',
          component: () => import("@/components/ventas/AllVentas.vue"),
          meta: { requiresAuth: true }
        },
        {
          path: '/inicio/usuarios',
          name: 'Usuarios',
          component: () => import("@/components/usuario/AllUsers.vue"),
          meta: { requiresAuth: true }
        },
        {
          path: '/inicio/dashboard',
          name: 'Dashboard',
          component: () => import('@/components/dashboard/dashboard.vue'),
          meta: { requiresAuth: true }
        },
      ]
    },
  ]
});

router.beforeEach(async (to, from, next) => {
  const user = sessionStorage.getItem('user');
  const token = sessionStorage.getItem('token');
  const refreshToken = sessionStorage.getItem('refresh_token');
  const authStore = useAuthStore();

  // Si la ruta requiere ser admin
  if (to.path === '/inicio/usuarios') {
    if (!user) {
      next({ name: 'login' });
      return;
    }
    const userObj = JSON.parse(user);
    if (userObj.rol !== 'admin') {
      next({ name: 'inicio' });
      return;
    }
  }

  if (to.meta.requiresAuth) {
    if (!user) {
      next({ name: 'login' });
    } else if (!token && refreshToken) {
      const refreshed = await authStore.refreshAccessToken();
      if (refreshed) {
        next();
      } else {
        next({ name: 'login' });
      }
    } else if (!token && !refreshToken) {
      next({ name: 'login' });
    } else {
      next();
    }
  } else if (user && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'inicio' });
  } else {
    next();
  }
});

export default router;