import { createRouter, createWebHistory } from "vue-router"

import FrontPage from "../views/FrontPage.vue"
import Login from "../views/Login.vue"
import Register from "../views/Register.vue"
import MoviePage from "../views/MoviePage.vue"
import ActorPage from "../views/ActorPage.vue"
import ProfilePage from "../views/ProfilePage.vue"
import GenrePage from "../views/GenrePage.vue"
import Movies from "../views/Movies.vue"
import SearchPage from "../views/SearchPage.vue"
import SavedOfUser from "@/views/SavedOfUser.vue"

const routes = [
  { 
    path: "/", 
    component: FrontPage,
    name: 'home'
  },
  { 
    path: "/login", 
    component: Login,
    name: 'login',
    meta: { guestOnly: true }
  },
  { 
    path: "/register", 
    component: Register,
    name: 'register',
    meta: { guestOnly: true }
  },
  { 
    path: "/movie/:id", 
    component: MoviePage,
    name: 'movie'
  },
  { 
    path: "/actor/:id", 
    component: ActorPage,
    name: 'actor'
  },
  { 
    path: "/profile", 
    component: ProfilePage,
    name: 'profile',
    meta: { requiresAuth: true }
  },
  { 
    path: "/genre/:id", 
    component: GenrePage,
    name: 'genre'
  },
  { 
    path: "/movies", 
    component: Movies,
    name: 'movies'
  },
  { 
    path: "/search", 
    component: SearchPage,
    name: 'search'
  },
  { 
    path: "/saved", 
    component: SavedOfUser,
    name: 'saved',
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token
  
  // Проверка защищённых маршрутов
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // Проверка маршрутов только для гостей
  if (to.meta.guestOnly && isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

export default router