<template>
    <div>
      <h1 class="text-3xl font-bold underline">Hello world!</h1>
      <div>
        <input v-model="message" placeholder="Type a message" @keyup.enter="sendMessage" />
        <button @click="sendMessage">Send</button>
      </div>
      <div>
        <h2 class="text-xl font-semibold mt-4">Messages:</h2>
        <ul>
          <li v-for="(msg, index) in messages" :key="index">{{ msg }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  
  // Reactive state
  const message = ref('');
  const messages = ref([]);
  let chatSocket = null;
  
  // Connect to WebSocket
  const connectWebSocket = () => {
    chatSocket = new WebSocket('ws://127.0.0.1:8000/ws/chat/your_room_name/'); // Replace 'your_room_name' with your room name
  
    chatSocket.onopen = () => {
      console.log('WebSocket connection established.');
    };
  
    chatSocket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      messages.value.push(data.message); // Add received message to the list
    };
  
    chatSocket.onclose = () => {
      console.log('WebSocket connection closed.');
    };
  
    chatSocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  };
  
  // Send message through WebSocket
  const sendMessage = () => {
    if (message.value.trim() && chatSocket) {
      chatSocket.send(
        JSON.stringify({
          message: message.value,
        })
      );
      message.value = ''; // Clear input after sending
    }
  };
  
  // Lifecycle hooks
  onMounted(() => {
    connectWebSocket();
  });
  
  onUnmounted(() => {
    if (chatSocket) {
      chatSocket.close();
    }
  });
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>