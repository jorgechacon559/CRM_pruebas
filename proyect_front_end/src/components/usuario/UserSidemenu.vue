<script setup>
import { reactive } from 'vue';

const buttons = reactive([
    {
        'title': 'Productos',
        'link': '/inicio/productos',
    },
    {
        'title': 'Ventas',
        'link': '/inicio/ventas',
    },
    {
        'title': 'Usuarios',
        'link': '/inicio/usuarios',
    },
])
</script>
<template>
    <aside>
        <router-link v-for="button in buttons" :to="button.link">{{ button.title }}</router-link>
    </aside>
</template>
<style scoped lang="scss">
aside {
    display: grid;
    grid-auto-rows: max-content;

    padding: .25rem .75rem;
}
</style>