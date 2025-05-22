import { createRouter, createMemoryHistory } from "vue-router";

export const router = createRouter({
  history: createMemoryHistory(import.meta.env.BASE_URL || '/'),
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
      ]
    },
  ]
});

router.beforeEach((to, from, next) => {
  const user = sessionStorage.getItem('user');
  if (to.meta.requiresAuth && !user) {
    next({ name: 'login' });
  } else if (user && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'inicio' });
  } else {
    next();
  }
});

export default router;