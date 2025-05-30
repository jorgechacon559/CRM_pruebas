<template>
  <div class="register-bg">
    <div class="register-container">
      <form class="register-form" @submit.prevent="register">
        <h2 class="form-title">Crear cuenta</h2>
        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
        <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
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
            :class="{'form-control': true, 'input-error': emailError}"
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
            :class="{'form-control': true, 'input-error': passwordError}"
            required
          />
        </div>
        <div class="form-group">
          <label for="password2">Confirmar contraseña</label>
          <input
            type="password"
            id="password2"
            v-model="password2"
            placeholder="Confirma tu contraseña"
            :class="{'form-control': true, 'input-error': passwordError}"
            required
          />
        </div>
        <button type="submit" class="btn-primary">Registrarse</button>
      </form>
      <div class="register-switch">
        <span>¿Ya tienes una cuenta?</span>
        <button class="btn-secondary" @click="$router.push('/login')">Iniciar sesión</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('')
const apellido = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const emailError = ref(false)
const passwordError = ref(false)
const authStore = useAuthStore()

async function register() {
  errorMsg.value = ''
  successMsg.value = ''
  emailError.value = false
  passwordError.value = false

  if (password.value !== password2.value) {
    errorMsg.value = "Las contraseñas no coinciden"
    passwordError.value = true
    return
  }
  try {
    const response = await authStore.register(name.value, apellido.value, email.value, password.value)
    // Asegúrate de que tu backend devuelva un campo 'success' booleano en el registro exitoso
    if (response?.success === true || response?.msg?.toLowerCase().includes('exitoso')) {
      // Solo si fue exitoso, redirige
      router.push({ path: '/login', query: { msg: '¡Registro exitoso! Ahora puedes iniciar sesión.' } })
    } else if (response?.msg?.toLowerCase().includes('correo')) {
      errorMsg.value = "El correo ya está registrado"
      emailError.value = true
    } else {
      errorMsg.value = "Error al registrar. Verifica tus datos."
    }
  } catch (error) {
      console.log('Error en registro:', error)
      // Intenta leer el mensaje de varias formas
      const msg =
        error?.response?.data?.msg ||
        error?.response?.data?.message ||
        error?.response?.data?.mensaje || // <-- agrega esta línea
        error?.message ||
        '';
      console.log('Mensaje recibido:', msg);
      if (msg.toLowerCase().includes('correo') || msg.toLowerCase().includes('existe')) {
        errorMsg.value = "El correo ya está registrado";
        emailError.value = true;
      } else {
        errorMsg.value = "Error al registrar. Verifica tus datos.";
      }
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
  border-radius: 1.5rem;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  width: 600px;
}

.input-error {
  border: 2px solid #d32f2f !important;
  background: #fff0f0;
}
.error-msg {
  color: #d32f2f;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
}
.success-msg {
  color: #2e7d32;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
  background: #e6fbe6;
  border-radius: 0.5rem;
  padding: 0.5rem 0;
}
@media (max-width: 600px) {
  .register-container {
    width: 100vw !important;
    min-width: 0;
    padding: 0 0.5rem;
  }
  .register-form {
    width: 100vw !important;
    min-width: 0;
    padding: 1rem 0.5rem !important;
  }
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
  width: 100%;
  display: block;
}

.btn-primary:hover {
  background-color: #1e40af;
}

.register-switch {
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
</style>