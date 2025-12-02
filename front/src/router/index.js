import { createRouter, createWebHistory } from "vue-router";

import FrontPage from "../views/FrontPage.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
// import Profile from "../views/Profile.vue";
// import ActorPage from "../views/ActorPage.vue";
// import GenrePage from "../views/GenrePage.vue";

const routes = [
  { 
    path: "/", 
    component: FrontPage,
    name: 'home'
  },
  { 
    path: "/login", 
    component: Login,
    name: 'login'
  },
  { 
    path: "/register", 
    component: Register,
    name: 'register'
  },
  // { 
  //   path: "/profile", 
  //   component: Profile,
  //   name: 'profile'
  // },
  // { path: "/actor/:id", component: ActorPage },
  // { path: "/genre/:id", component: GenrePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// router.beforeEach((to, from, next) => {
//   // Проверка аутентификации
//   const isAuthenticated = localStorage.getItem('token') // или другой метод проверки
  
//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next('/login')
//   } else {
//     next()
//   }
// });

export default router;