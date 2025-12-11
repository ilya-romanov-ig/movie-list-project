<template>
  <v-app>
    <v-main>
      <v-container fluid class="page-wrapper">
        <slot></slot>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background-color: #121212; /* тёмно-серый фон */
  color: #ffffff; /* белый текст */
  padding-top: 16px;
  padding-bottom: 16px;
}
</style>
