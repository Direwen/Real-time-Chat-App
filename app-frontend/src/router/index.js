// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Chats from '../views/Chats.vue';
import Chat from '../views/Chat.vue';
import { useAppStore } from '../store/appStore';

const requireUnauthenticated = async (to, from, next) => {
  const appStore = useAppStore();
  await appStore.getUser();

  if (appStore.isActive) {
    return next('/chats');
  }
  next();
};

const requireAuthenticated = async (to, from, next) => {
  const appStore = useAppStore();
  await appStore.getUser();

  if (!appStore.isActive) {
    return next('/');
  }
  next();
}

const validateChatId = (to, from, next) => {
  const appStore = useAppStore();

  const targetChat = appStore.chats.find(chat => chat.id == to.params.id);
  if (targetChat) {
    appStore.activeChat = targetChat;
    next();
  } else {
    next("/chats");
  }
}

const routes = [
  { path: '/', component: Login, beforeEnter: requireUnauthenticated },
  { path: '/chats', component: Chats },
  { path: '/chats/:id', name:"chat", component: Chat },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});;

export default router;