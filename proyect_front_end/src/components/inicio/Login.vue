<template>
  <div class="login-bg">
    <div class="login-container">
      <form class="login-form" @submit.prevent="login">
        <h2>Iniciar sesión</h2>
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input
            type="email"
            id="email"
            v-model="correo"
            placeholder="Tu correo electrónico"
            required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="password">Contraseña</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Tu contraseña"
            required
            class="form-control"
          />
        </div>
        <button type="submit" class="btn-primary">Ingresar</button>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
      </form>
      <div class="login-switch">
        <span>¿No tienes una cuenta?</span>
        <button class="btn-secondary" @click="$router.push('/register')">Registrarse</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

// Estado para los campos del formulario y mensajes de error
const correo = ref('');
const password = ref('');
const errorMsg = ref('');
const authStore = useAuthStore();

// Maneja el envío del formulario de login
async function login() {
    try {
        await authStore.login(correo.value, password.value);
    } catch (error) {
        // Muestra mensaje de error si las credenciales son incorrectas
        errorMsg.value = "Correo o contraseña incorrectos";
    } finally {
        // Limpia los campos después de intentar iniciar sesión
        correo.value = '';
        password.value = '';
    }
}
</script>

<style scoped>
.login-bg {
  min-height: 1vh;
  background: linear-gradient(120deg, #f7f8fa 60%, #e0e7ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 1.5rem;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  width: 600px
}

.login-form {
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

.login-form h2 {
  text-align: center;
  color: #2563eb;
  font-weight: 700;
  margin-bottom: 0.5rem;
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
  box-sizing: border-box;
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
}

.btn-primary:hover {
  background-color: #1e40af;
}

.login-switch {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.98rem;
  color: #444;
}
.btn-secondary {
  margin-left: 0.5rem;
  background: #fff;
  color: #2563eb;
  border: 1.5px solid #2563eb;
  border-radius: 0.7rem;
  padding: 0.5rem 1.1rem;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border 0.2s;
}
.btn-secondary:hover {
  background: #2563eb;
  color: #fff;
}
.error-msg {
  color: #d32f2f;
  margin-top: 0.5rem;
  text-align: center;
}
</style>