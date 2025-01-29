<template>
  <div>
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { RouterView } from 'vue-router';
import { useAppStore } from './store/appStore';

const appStore = useAppStore()

onMounted(async () => {
  await appStore.getUser()
})
</script>