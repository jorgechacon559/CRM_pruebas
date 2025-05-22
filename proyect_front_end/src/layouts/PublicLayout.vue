<template>
  <div class="public-bg">
    <div class="public-container">
      <header>
        <h1>Bienvenido al CRM</h1>
      </header>
      <div class="wrapper">
        <RouterView />
        <div class="auth-links">
          <RouterLink to="/login" class="auth-button">Iniciar sesión</RouterLink>
          <RouterLink to="/register" class="auth-button secondary">Registrarse</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.public-bg {
  min-height: 0vh;
  background: linear-gradient(120deg, #f7f8fa 60%, #e0e7ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.public-container {
  width: 100%;
  max-width: 420px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px rgba(37,99,235,0.08);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

header {
  background: transparent;
  padding: 2rem 2rem 1rem 2rem;
  border-bottom: none;
}

h1 {
  margin: 0;
  color: #2563eb;
  text-align: center;
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -1px;
  text-transform: none;
}

.wrapper {
  padding: 0rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}

.auth-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.auth-button {
  display: inline-block;
  padding: 0.85rem 2rem;
  background-color: #2563eb;
  color: #fff;
  text-decoration: none;
  border-radius: 0.7rem;
  font-weight: 700;
  font-size: 1.05rem;
  border: none;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);
  transition: background 0.2s, color 0.2s;
}

.auth-button.secondary {
  background: #f1f5ff;
  color: #2563eb;
  border: 1.5px solid #b6d0fa;
}

.auth-button:hover {
  background: #1e40af;
  color: #fff;
}

.auth-button.secondary:hover {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}
</style>