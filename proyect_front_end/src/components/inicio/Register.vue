<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useMessageStore } from '@/stores/message'

const messageStore = useMessageStore()
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

const minLength = computed(() => password.value.length >= 8)
const hasUpper = computed(() => /[A-Z]/.test(password.value))
const hasLower = computed(() => /[a-z]/.test(password.value))
const hasNumber = computed(() => /\d/.test(password.value))
const hasSymbol = computed(() => /[!@#$%^&*()_\-+=\[\]{};':"\\|,.<>/?`~]/.test(password.value))

const passwordStrength = computed(() => {
  let score = 0
  if (minLength.value) score++
  if (hasUpper.value) score++
  if (hasLower.value) score++
  if (hasNumber.value) score++
  if (hasSymbol.value) score++
  if (password.value.length >= 16 && hasSymbol.value && hasUpper.value && hasLower.value && hasNumber.value) score++
  return score
})

const strengthLabel = computed(() => {
  switch (passwordStrength.value) {
    case 0: case 1: return 'Débil'
    case 2: return 'Regular'
    case 3: return 'Fuerte'
    case 4: return 'Muy fuerte'
    case 5: return 'Excelente'
    case 6: return 'Irrompible'
    default: return ''
  }
})

const barColor = computed(() => {
  switch (passwordStrength.value) {
    case 0: case 1: return '#e53e3e' // rojo
    case 2: return '#f59e42' // naranja
    case 3: return '#fbbf24' // amarillo
    case 4: return '#22c55e' // verde
    case 5: return '#15803d' // verde oscuro
    case 6: return '#065f46' // más oscuro aún para "Irrompible"
    default: return '#e5e7eb'
  }
})

const canRegister = computed(() =>
  minLength.value && hasUpper.value && hasLower.value && hasNumber.value && hasSymbol.value && password.value === password2.value
)

async function register() {
  errorMsg.value = ''
  successMsg.value = ''
  emailError.value = false
  passwordError.value = false

  if (!canRegister.value) {
    errorMsg.value = "La contraseña no cumple los requisitos o no coincide."
    passwordError.value = true
    return
  }
  try {
    const response = await authStore.register(name.value, apellido.value, email.value, password.value);
    const res = response.data

    if (
      res?.usuario ||
      res?.mensaje?.toLowerCase().includes('éxito') ||
      res?.mensaje?.toLowerCase().includes('exito')
    ) {
      messageStore.setMessage('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
      router.push({ path: '/login' })
    } else if (res?.mensaje?.toLowerCase().includes('existe')) {
      errorMsg.value = "El correo ya está registrado"
      emailError.value = true
    } else {
      errorMsg.value = "Error al registrar. Verifica tus datos."
    }
  } catch (error) {
    const msg =
      error?.response?.data?.msg ||
      error?.response?.data?.message ||
      error?.response?.data?.mensaje ||
      error?.message ||
      '';
    if (msg.toLowerCase().includes('correo') || msg.toLowerCase().includes('existe')) {
      errorMsg.value = "El correo ya está registrado";
      emailError.value = true;
    } else {
      errorMsg.value = "Error al registrar. Verifica tus datos.";
    }
  }
}
</script>

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
            autocomplete="new-password"
          />
          <div class="password-checklist">
            <div :class="{ ok: minLength }">La contraseña debe contener mínimo 8 caracteres.</div>
            <div :class="{ ok: hasUpper }">Al menos una letra mayúscula.</div>
            <div :class="{ ok: hasLower }">Al menos una letra minúscula.</div>
            <div :class="{ ok: hasNumber }">Al menos un número.</div>
            <div :class="{ ok: hasSymbol }">Al menos un símbolo especial.</div>
            <div :class="{ ok: password.length >= 16 }">16 caracteres o más para máxima seguridad.</div>
          </div>
          <div class="password-strength">
            <div
              class="bar"
              :style="{
                width: (passwordStrength * 16.66) + '%',
                background: barColor
              }"
            ></div>
            <span class="label">{{ strengthLabel }}</span>
          </div>
        </div>
        <div class="form-group">
          <label for="password2">Confirmar contraseña</label>
          <input
            type="password"
            id="password2"
            v-model="password2"
            placeholder="Confirma tu contraseña"
            :class="{
              'form-control': true,
              'input-error': password2 && password !== password2
            }"
            required
            autocomplete="new-password"
          />
          <div v-if="password2 && password !== password2" class="password-mismatch">
            Las contraseñas no coinciden.
          </div>
        </div>
        <button type="submit" class="btn-primary" :disabled="!canRegister">Registrarse</button>
      </form>
      <div class="register-switch">
        <span>¿Ya tienes una cuenta?</span>
        <button class="btn-secondary" @click="$router.push('/login')">Iniciar sesión</button>
      </div>
    </div>
  </div>
</template>

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

.password-checklist .ok {
  color: #2563eb;
  font-weight: 600;
}
.password-strength {
  margin-top: 0.3rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.password-strength .bar {
  height: 8px;
  border-radius: 4px;
  transition: width 0.3s, background 0.3s;
  min-width: 40px;
  max-width: 200px;
  width: 0;
}
.password-strength .label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2563eb;
}
.password-mismatch {
  color: #e53e3e;
  font-size: 0.95rem;
  margin-top: 0.2rem;
}
</style>