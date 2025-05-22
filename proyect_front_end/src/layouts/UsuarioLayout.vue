<script setup>
import UserHeader from '@/components/usuario/UserHeader.vue'
import UserSidemenu from '@/components/usuario/UserSidemenu.vue';
import chatbot from '@/components/chatbot/chatbot.vue';
</script>
<template>
  <div class="container">
    <UserHeader class="header" />
    <UserSidemenu class="aside" />
    <router-view class="content" />
    <chatbot />
  </div>
</template>
<style scoped lang="scss">
.container {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
  grid-template-areas:
    "header header"
    "aside content";
  grid-template-columns: 13rem 0.5fr;
  background: linear-gradient(120deg, #bacced 60%, #e0e7ff 100%);
  padding: 2.5rem 0;

  /* Espaciado general entre áreas */
  column-gap: 2rem;
  row-gap: 2rem;

  .header {
    grid-area: header;
    background: #fff;
    border-radius: 1.5rem 1.5rem 1.5rem 1.5rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04);
    padding: 1.5rem 2rem 1rem 2rem;
    margin-bottom: 0;
    margin-left: 2rem;
    margin-right: 2rem;
  }

  .aside {
    grid-area: aside;
    background: #fff;
    border-radius: 1.5rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.04);
    padding: 2rem 1rem;
    min-width: 4rem;
    height: fit-content;
    margin-left: 2rem;
    margin-bottom: 2rem;
  }

  .content {
    grid-area: content;
    background: #fff;
    border-radius: 1.5rem;
    box-shadow: 0 4px 24px rgba(26,115,232,0.07);
    padding: 2rem 2.5rem 2.5rem 2.5rem;
    min-height: 70vh;
    margin-right: 2rem;
    margin-bottom: 2rem;
  }
}
</style>