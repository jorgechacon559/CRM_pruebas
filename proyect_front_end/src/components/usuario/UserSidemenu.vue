<script setup>
const buttons = [
    { title: 'Productos', link: '/inicio/productos' },
    { title: 'Ventas', link: '/inicio/ventas' },
    { title: 'Usuarios', link: '/inicio/usuarios' },
    { title: 'Dashboard', link: '/inicio/dashboard' }
];
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