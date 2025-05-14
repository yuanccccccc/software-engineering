import axios from "axios";

const instance = axios.create({
  baseURL: "http://127.0.0.1:5000", // 后端 Flask 服务地址
  timeout: 5000, // 请求超时时间
});

// 请求拦截器：添加 Token 到请求头
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器：处理错误
instance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token 过期或未授权，跳转到登录页面
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default instance;
