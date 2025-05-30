<template>
  <div v-if="show" :class="['toast', type]">{{ message }}</div>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ message: String, type: String, show: Boolean })
</script>

<style scoped>
.toast {
  position: fixed;
  top: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  padding: 1rem 2rem;
  border-radius: 0.7rem;
  font-weight: 600;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);
  animation: fadeInOut 2.5s;
}
.toast.success {
  background: #e6fbe6;
  color: #2e7d32;
  border: 2px solid #2e7d32;
}
.toast.error {
  background: #fff0f0;
  color: #d32f2f;
  border: 2px solid #d32f2f;
}
@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { opacity: 0; }
}
</style>