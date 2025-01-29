// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Users from '../views/Users.vue';
import Chat from '../views/Chat.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/users', component: Users },
  { path: '/chat/:id', name:"chat", component: Chat },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});;

export default router;