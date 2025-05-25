<template>
  <!-- Chatbot UI principal -->
  <form class="chat-bot" @submit.prevent="submitData">
    <div class="chat-bot-container" :class="{ compact: !state }">
      <div class="chat-bot-view" :class="{ 'active': state }">
        <div class="pantalla">
          <!-- Renderiza los mensajes del chat -->
          <div class="message" v-for="mensaje in mensajes" :class="{ 'toRight': mensaje.usuario }">
            <p>{{ mensaje.content }}</p>
          </div>
          <!-- Indicador de respuesta generándose -->
          <div v-if="!inputEnable" class="gen-answer">
            <p>Generando respuesta</p>
            <div :style="{ '--Delay': '100ms' }"></div>
            <div :style="{ '--Delay': '200ms' }"></div>
            <div :style="{ '--Delay': '300ms' }"></div>
          </div>
        </div>
        <div class="mensaje">
          <textarea v-model="actualMsg" placeholder="Escribe tu mensaje..." :disabled="!inputEnable"></textarea>
          <button type="submit" :disabled="!inputEnable">Enviar</button>
        </div>
      </div>
      <div class="buttons-contenedor">
        <button type="button" @click="mensajes = []" v-if="state">Limpiar chat</button>
        <button type="button" @click="state = !state">{{ state ? 'Cerrar' : 'Abrir' }} chat</button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';
import { useChatbotStore } from '@/stores/chatBot';

const chatbot = useChatbotStore();

const state = ref(false) // Estado de visibilidad del chat
const actualMsg = ref('') // Mensaje actual del usuario
const mensajes = ref([]) // Historial de mensajes
const inputEnable = ref(true); // Controla si el input está habilitado

// Envía el mensaje y gestiona la respuesta del bot
const submitData = async () => {
  if (!inputEnable.value) return;
  if (!actualMsg.value) return;

  inputEnable.value = false;
  mensajes.value.push({ 'usuario': true, 'content': actualMsg.value });

  const item = { 'consulta': actualMsg.value };
  actualMsg.value = '';
  const response = await chatbot.addItemBot({ 'option': 'chatbot', item });
  mensajes.value.push({ 'usuario': false, 'content': response.respuesta });

  inputEnable.value = true;
}
</script>

<style scoped lang="scss">
/* Estilos para el chatbot flotante y sus elementos */
.chat-bot {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 2000;
  background: transparent;
  border: none;
  box-shadow: none;
  margin: 0;
  padding: 0;
  width: auto;
}

.chat-bot-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.chat-bot-container.compact {
  width: auto !important;
  min-width: 0 !important;
  min-height: 0 !important;
  padding: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
}

.chat-bot-container.compact .chat-bot-view {
  display: none !important;
}

.chat-bot-view {
  background: #fff;
  border-radius: 1.2rem;
  box-shadow: 0 4px 24px rgba(37,99,235,0.10);
  width: 340px;
  max-width: 95vw;
  min-height: 60px;
  transition: box-shadow 0.2s, max-height 0.3s;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
  transform: translateY(20px) scale(0.98);
  transition: opacity 0.2s, transform 0.2s;
  margin-bottom: 0.5rem;

  &.active {
    opacity: 1;
    pointer-events: auto;
    transform: translateY(0) scale(1);
    min-height: 500px;
    box-shadow: 0 8px 32px rgba(37,99,235,0.18);
    border: 1.5px solid #e5e7eb;
  }
}

.pantalla {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem 1rem 0.5rem 1rem;
  overflow-y: auto;
  max-height: 400px;
  font-size: 0.98rem;
  color: #222;
  background: #f7f8fa;
}

.message {
  align-self: flex-start;
  max-width: 75%;
  min-width: 60px;
  word-break: break-word;
  white-space: pre-line;
  padding: 0.5rem 0.9rem;
  background-color: #2563eb;
  border-radius: 1.1rem 1.1rem 1.1rem 0.4rem;
  color: #fff; // Por defecto blanco para el bot
  line-height: 1.5;
  font-size: 1rem;
  text-align: left;
  box-shadow: 0 2px 8px rgba(37,99,235,0.04);

  p {
    margin: 0;
    color: inherit; // Usa el color del padre
    width: 100%;
    word-break: break-word;
  }

  &.toRight {
    align-self: flex-end;
    background-color: #4caf50;
    border-radius: 1.1rem 1.1rem 0.4rem 1.1rem;
    color: #fff;
    text-align: left;
  }
}

.mensaje {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  padding: 0.7rem 1rem 1rem 1rem;
  background: #fff;
  border-top: 1.5px solid #e5e7eb;
}

textarea {
  flex: 1;
  resize: none;
  padding: 0.7rem 1rem;
  border-radius: 0.7rem;
  border: 1.5px solid #e5e7eb;
  font-size: 1rem;
  background: #f7f8fa;
  color: #222;
  transition: border 0.2s;
  min-height: 38px;
  max-height: 80px;
  outline: none;

  &:focus {
    border-color: #2563eb;
    background: #fff;
  }
}

.mensaje button[type="submit"] {
  background-color: #2563eb;
  color: #fff;
  border: none;
  border-radius: 0.7rem;
  padding: 0.7rem 1.2rem;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px rgba(37,99,235,0.10);

  &:hover {
    background-color: #1e40af;
  }

  &:disabled {
    background: #b6c5e6;
    cursor: not-allowed;
  }
}

.buttons-contenedor {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.2rem;

  button {
    background-color: #f1f5ff;
    color: #2563eb;
    border: 1.5px solid #b6d0fa;
    border-radius: 0.7rem;
    padding: 0.5rem 1.1rem;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s, border 0.2s;

    &:hover {
      background: #2563eb;
      color: #fff;
      border-color: #2563eb;
    }
  }
}

.gen-answer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2563eb;
  font-style: italic;

  div {
    background-color: #b6d0fa;
    border-radius: 50%;
    animation: flying 800ms ease-in-out var(--Delay, 0s) infinite;
    width: 0.5rem;
    height: 0.5rem;
  }
}

@keyframes flying {
  0%, 100% { transform: translateY(0rem);}
  50% { transform: translateY(-0.4rem);}
}
</style>