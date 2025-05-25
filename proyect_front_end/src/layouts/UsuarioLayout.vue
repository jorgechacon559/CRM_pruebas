<script setup>
import UserHeader from '@/components/usuario/UserHeader.vue'
import UserSidemenu from '@/components/usuario/UserSidemenu.vue';
import chatbot from '@/components/chatbot/chatbot.vue';
</script>
<template>
  <div class="layout-bg">
    <div class="container">
      <UserHeader class="header" />
      <UserSidemenu class="aside" />
      <router-view class="content" />
      <chatbot />
    </div>
  </div>
</template>
<style scoped lang="scss">
.layout-bg {
  min-height: 100vh;
  background: linear-gradient(120deg, #bacced 60%, #e0e7ff 100%);
  padding: 2.5rem 0;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.container {
  display: grid;
  grid-template-rows: auto 1fr;
  grid-template-areas:
    "header header"
    "aside content";
  grid-template-columns: 13rem 1fr;
  column-gap: 2rem;
  row-gap: 2rem;
  width: 100%;
  max-width: 1400px;
  min-height: 90vh;
  padding: 0 2rem;
  box-sizing: border-box;
}

.header {
  grid-area: header;
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.04);
  padding: 1.5rem 2rem 1rem 2rem;
  width: 100%;
  box-sizing: border-box;
}

.aside {
  grid-area: aside;
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 2px 16px rgba(0,0,0,0.04);
  padding: 2rem 1rem;
  min-width: 4rem;
  height: fit-content;
}

.content {
  grid-area: content;
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 4px 24px rgba(26,115,232,0.07);
  padding: 2rem 2.5rem 2.5rem 2.5rem;
  min-height: 70vh;
  width: 100%;
  overflow-x: auto;
  box-sizing: border-box;
}
</style>