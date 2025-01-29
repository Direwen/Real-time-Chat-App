import { defineStore } from 'pinia'
import AxiosInstance from "../axiosInstance"

export const useAppStore = defineStore('app', {
  state: () => ({
    loading: false,
    user: null,
    isActive: false,
    chats: null,
    activeChat: null
  }),
  actions: {
    async login(username, password) {
      
      await this.handleAsync(async () => {  // Use 'this.handleAsync' after moving it inside actions
        const res = await AxiosInstance.post("auth/jwt/create", {
          username: username,
          password: password
        });

        this.saveToken(res.data.refresh, res.data.access)
  
      });
    },

    async listChats() {

      await this.handleAsync(async () => {
        const res = await AxiosInstance.get("api/chats")
        console.log(res.data)
        this.chats = res.data
      })

    },

    async getUser() {
      if (localStorage.getItem("token") && !this.user) {
        await this.handleAsync(async () => {
          const res = await AxiosInstance.get("auth/users/me");
          this.user = res.data
          this.isActive = true
    
        });
      } else {
        console.log('nah')
      }
    },

    saveToken(refresh, access) {
      localStorage.setItem('token', access)
      localStorage.setItem('refresh', refresh)
    },

    removeToken() {
      localStorage.removeItem('token')
      localStorage.removeItem('refresh')
    },

    removeUserData() {
      this.user = null;
      this.removeToken();
      this.isActive = false;
    },

    async handleAsync(task, errorMessage = "Something went wrong", loading = true) {
      this.loading = loading;

      try {
          const result = await task();
          return result;
      } catch (error) {
          throw error;
      } finally {
          this.loading = false;
      }
    }
  }
});
