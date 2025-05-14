<template>
  <div class="register">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" type="text" placeholder="用户名" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">注册</button>
    </form>
    <p>已有账号？<router-link to="/login">登录</router-link></p>
  </div>
</template>

<script>
import axios from "@/lib/axios";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async handleRegister() {
      console.log("Username:", this.username); // 打印用户名
      console.log("Password:", this.password); // 打印密码
      try {
        await axios.post("/auth/register", {
          username: this.username,
          password: this.password,
        });
        alert("注册成功，请登录！");
        this.$router.push("/login"); // 注册成功后跳转到登录页面
      } catch (error) {
        alert("注册失败，请重试");
      }
    },
  },
};
</script>
