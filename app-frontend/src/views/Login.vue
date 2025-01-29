<template>
    <div class="flex flex-col gap-4 p-4 max-w-sm mx-auto">

      {{ appStore.user }}

      <input 
        v-model="username" 
        type="text" 
        placeholder="Username" 
        class="border p-2 rounded-md" 
      />
      <input 
        v-model="password" 
        type="password" 
        placeholder="Password" 
        class="border p-2 rounded-md" 
      />
      <button 
        @click="login" 
        class="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600">
        Login
      </button>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useAppStore } from "../store/appStore";
import { useRouter } from "vue-router";
  
  const appStore = useAppStore();
  const username = ref("");
  const password = ref("");
  const router = useRouter();

  const login = async () => {
    try {
      await appStore.login(username.value, password.value);
      await appStore.getUser()
      router.push("/users")
    } catch (error) {
      console.log(error)
    }

  };
  </script>
  