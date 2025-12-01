import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../components/HomePage.vue";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import ActorPage from "../components/ActorPage.vue";
import GenrePage from "../components/GenrePage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/actor/:id", component: ActorPage },
  { path: "/genre/:id", component: GenrePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
