<template>
  <div class="login">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="用户名" required />
      <input v-model="password" type="password" placeholder="密码" required />
      <button type="submit">登录</button>
    </form>
    <p>没有账号？<router-link to="/register">注册</router-link></p>
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
    async handleLogin() {
      console.log("Username:", this.username); // 打印用户名
      console.log("Password:", this.password); // 打印密码

      try {
        const response = await axios.post("/auth/login", {
          username: this.username,
          password: this.password,
        });
        const { token, role } = response.data;
        localStorage.setItem("token", token);
        localStorage.setItem("role", role);
        if (role === "admin") {
          this.$router.push("/admin"); // 管理员跳转到管理员页面
        } else {
          this.$router.push("/page1"); // 普通用户跳转到 page1
        }
      } catch (error) {
        alert("登录失败，请检查用户名和密码");
      }
    },
  },
};
</script>
