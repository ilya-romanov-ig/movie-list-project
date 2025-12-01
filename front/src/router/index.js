import { createRouter, createWebHistory } from "vue-router";

import FrontPage from "../views/FrontPage.vue";
// import Login from "../views/Login.vue";
// import Register from "../views/Register.vue";
// import ActorPage from "../views/ActorPage.vue";
// import GenrePage from "../views/GenrePage.vue";

const routes = [
  { path: "/", component: FrontPage },
  // { path: "/login", component: Login },
  // { path: "/register", component: Register },
  // { path: "/actor/:id", component: ActorPage },
  // { path: "/genre/:id", component: GenrePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
