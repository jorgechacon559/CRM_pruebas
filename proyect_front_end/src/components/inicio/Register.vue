<template>
  <div class="register-bg">
    <div class="register-container">
      <form class="register-form" @submit.prevent="register">
        <h2 class="form-title">Crear cuenta</h2>
        <div class="form-group">
          <label for="name">Nombre</label>
          <input
            type="text"
            id="name"
            v-model="name"
            placeholder="Tu nombre"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="apellido">Apellido</label>
          <input
            type="text"
            id="apellido"
            v-model="apellido"
            placeholder="Apellido"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Tu correo electrónico"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Crea una contraseña"
            class="form-control"
            required
          />
        </div>
        <div class="form-group">
          <label for="password2">Confirmar Contraseña</label>
          <input
            type="password"
            id="password2"
            v-model="password2"
            placeholder="Confirma tu contraseña"
            class="form-control"
            required
          />
        </div>
        <button type="submit" class="btn-primary">Registrarse</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const name = ref('')
const apellido = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const authStore = useAuthStore()

async function register() {
    try {
        await authStore.register(name.value, apellido.value, email.value, password.value)
    } catch (error) {
        console.error(error)
    } finally {
        name.value = ''
        apellido.value = ''
        email.value = ''
        password.value = ''
        password2.value = ''
    }
}
</script>

<style scoped>
.register-bg {
  min-height: 0vh;
  background: linear-gradient(120deg, #f7f8fa 60%, #e0e7ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.register-form {
  background-color: #fff;
  padding: 2.5rem 2.5rem 2rem 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px rgba(37,99,235,0.08);
  width: 370px;
  max-width: 95vw;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-title {
  text-align: center;
  margin-bottom: 0.5rem;
  color: #2563eb;
  font-weight: 700;
  font-size: 2rem;
  letter-spacing: -1px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #2563eb;
  font-weight: 600;
  font-size: 1rem;
}

.form-control {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 0.7rem;
  font-size: 1rem;
  background-color: #f7f8fa;
  color: #222;
  transition: border 0.2s;
}

.form-control:focus {
  border-color: #2563eb;
  outline: none;
  background: #fff;
}

.btn-primary {
  background-color: #2563eb;
  color: #fff;
  padding: 0.9rem 1.5rem;
  border: none;
  border-radius: 0.7rem;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);
  transition: background 0.2s;
  margin-top: 0.5rem;
  width: 100%;
  display: block;
}

.btn-primary:hover {
  background-color: #1e40af;
}
</style>