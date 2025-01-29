<template>
    <div class="p-4">
        <section v-if="!appstore.user" class="text-center text-gray-500">Please Log In</section>
        <section v-else>
            <ul class="space-y-2">
                <li 
                    v-for="chat in appstore.chats" 
                    :key="chat.id" 
                    class="p-2 border rounded-md shadow-sm bg-white">
                    <router-link :to="{name: 'chat', params:{id : chat.id}}">
                        {{ chat.user1.id === appstore.user.id ? chat.user2.username : chat.user1.username }}
                    </router-link>
                    
                    {{ chat.created_at }}
                </li>
            </ul>
        </section>
    </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useAppStore } from "../store/appStore";

const appstore = useAppStore();

onMounted(async () => {
    await appstore.listChats();
});
</script>
