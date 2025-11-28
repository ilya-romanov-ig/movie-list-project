<template>
  <v-app>
    <v-app-bar color="primary" density="compact">
      <v-app-bar-title>Мое приложение</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-card class="mx-auto" max-width="400">
          <v-card-title>Добро пожаловать!</v-card-title>
          <v-card-text>
            <v-btn color="primary" @click="count++">
              Счетчик: {{ count }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const count = ref(0)
</script>