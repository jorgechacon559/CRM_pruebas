<script setup>
import { useAuthStore } from '@/stores/auth';

const auth = useAuthStore();
const identity = auth.user;
const logout = () => {
    auth.logout();
}

</script>
<template>
    <header>
        <div class="container">
            <h1>CRM interno de ventas</h1>
            <div class="user__data">
                <button class="logout" @click="logout" aria-label="Cerrar sesión">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                        stroke-linecap="round" stroke-linejoin="round" width="24" height="24" stroke-width="2">
                        <path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2">
                        </path>
                        <path d="M9 12h12l-3 -3"></path>
                        <path d="M18 15l3 -3"></path>
                    </svg>
                </button>

                <h3 v-if="identity">{{ identity.nombre }} {{ identity.apellido }}</h3>
            </div>
        </div>
    </header>
</template>
<style scoped lang="scss">
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding: .5rem 2.1875rem;

    .user__data {
        display: grid;
        grid-template-columns: auto 1fr;
        align-items: center;
        gap: 0 .25rem;
        border-radius: 50%;
    }
}

.logout {
    background-color: transparent;
    border-radius: 50%;
    display: grid;
    place-items: center;
    aspect-ratio: 1;
    padding: .3125rem;
    border: .0625rem solid #cb8080;
    cursor: pointer;
    svg {
        color: rgba(152, 100, 100, 0.781);
    }
}
</style>