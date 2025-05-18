<template>
  <div class="auth-bg">
    <div class="content">
      <span class="title">
        <span class="title-gradient">登录</span>
      </span>
      <span class="angle1"></span>
      <span class="angle2"></span>
      <span class="angle3"></span>
      <span class="angle4"></span>
      <form @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="用户名" required />
        <input v-model="password" type="password" placeholder="密码" required />
        <button type="submit">登录</button>
      </form>
      <p class="switch-tip">
        没有账号？<router-link to="/register">注册</router-link>
      </p>
    </div>
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
      try {
        const response = await axios.post("/auth/login", {
          username: this.username,
          password: this.password,
        });
        const { token, role } = response.data;
        localStorage.setItem("token", token);
        localStorage.setItem("role", role);
        if (role === "admin") {
          this.$router.push("/admin");
        } else {
          this.$router.push("/page1");
        }
      } catch (error) {
        alert("登录失败，请检查用户名和密码");
      }
    },
  },
};
</script>

<style scoped>
.auth-bg {
  min-height: 100vh;
  background: #03044a;
  display: flex;
  align-items: center;
  justify-content: center;
}
.content {
  position: relative;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.3);
  padding: 40px 32px 32px 32px;
  width: 340px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  font-size: 2rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 32px;
  position: relative;
  z-index: 1;
}
.title-gradient {
  background: linear-gradient(90deg, #2870e8, #feed2c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.angle1,
.angle2,
.angle3,
.angle4 {
  position: absolute;
  width: 18px;
  height: 18px;
  border: 3px solid #feed2c;
  border-radius: 4px;
}
.angle1 {
  left: -8px;
  top: -8px;
  border-right: none;
  border-bottom: none;
}
.angle2 {
  right: -8px;
  top: -8px;
  border-left: none;
  border-bottom: none;
}
.angle3 {
  left: -8px;
  bottom: -8px;
  border-right: none;
  border-top: none;
}
.angle4 {
  right: -8px;
  bottom: -8px;
  border-left: none;
  border-top: none;
}
form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
input {
  border-radius: 6px;
  border: 1px solid #0d2451;
  background: #151456;
  color: #fff;
  padding: 10px 14px;
  font-size: 1rem;
  outline: none;
  transition: border 0.2s;
}
input:focus {
  border: 1.5px solid #feed2c;
}
button {
  background: linear-gradient(90deg, #2870e8, #feed2c);
  color: #151456;
  border: none;
  border-radius: 6px;
  padding: 10px 0;
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.3s;
}
button:hover {
  background: linear-gradient(90deg, #feed2c, #2870e8);
}
.switch-tip {
  margin-top: 18px;
  color: #fff;
  font-size: 0.95rem;
}
.switch-tip a {
  color: #feed2c;
  text-decoration: underline;
}
</style>
