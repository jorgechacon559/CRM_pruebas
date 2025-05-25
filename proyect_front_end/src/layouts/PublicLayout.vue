<template>
  <div class="public-bg">
    <div class="public-container">
      <header>
        <h1>Bienvenido al CRM</h1>
      </header>
      <div class="wrapper">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>
.public-bg {
  background: linear-gradient(120deg, #f7f8fa 60%, #e0e7ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.public-container {
  width: 100%;
  max-width: 800px;
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
}

.wrapper {
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1.5rem;
}
</style>