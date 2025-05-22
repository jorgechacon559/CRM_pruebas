import './assets/main.css'

import { createApp } from 'vue'
import router from './router'
import { createPinia } from 'pinia'
import App from './App.vue'
import '@/api/axios'
import { useAuthStore } from './stores/auth'

const pinia = createPinia()
const app = createApp(App)


app.use(pinia)
app.use(router)

//Inicializamos el sotre
const autStore = useAuthStore()
autStore.initialize()

app.mount('#app')
