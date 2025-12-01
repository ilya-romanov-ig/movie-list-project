import { createApp } from "vue";
import App from "./App.vue";

import vuetify from "./plugins/vuetify";
import router from "./router";

import { createPinia } from "pinia";
import { useAuthStore } from "./stores/auth";

import APIClient from "./api/apiClient";
import { API_KEY } from "./api/useApi";

const app = createApp(App);

const pinia = createPinia();
app.use(pinia);

app.provide(
  API_KEY,
  new APIClient({
    baseURL: "https://api.example.com",
    getToken: async () => {
      const auth = useAuthStore();
      return auth.token;
    },
    onError: (error) => {
      console.error("API ERROR:", error);
    },
  })
);

app.use(router);

app.use(vuetify);

app.mount("#app");
