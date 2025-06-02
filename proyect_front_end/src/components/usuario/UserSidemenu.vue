<script setup>
import { ref } from 'vue';

const user = ref(null);
if (sessionStorage.getItem('user')) {
  user.value = JSON.parse(sessionStorage.getItem('user'));
}

const buttons = [
    { title: 'Productos', link: '/inicio/productos' },
    { title: 'Ventas', link: '/inicio/ventas' },
    { title: 'Dashboard', link: '/inicio/dashboard' }
];
if (user.value && user.value.rol === 'admin') {
  buttons.splice(2, 0, { title: 'Usuarios', link: '/inicio/usuarios' });
}
</script>

<template>
    <aside>
        <router-link v-for="button in buttons" :key="button.link" :to="button.link">
            {{ button.title }}
        </router-link>
    </aside>
</template>
<style scoped lang="scss">
aside {
    display: grid;
    grid-auto-rows: max-content;
    padding: .25rem .75rem;
}
</style>