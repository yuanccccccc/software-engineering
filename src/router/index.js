import Vue from "vue";
import Router from "vue-router";
import home from "@/views/home";

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      redirect: "/Login",
    },
    {
      path: "/home",
      name: "home",
      component: home,
      redirect: "/page1",
      children: [
        {
          path: "/admin",
          name: "Admin",
          component: () => import("@/views/Admin.vue"),
          meta: { requiresAuth: true, role: "admin" }, // 需要管理员权限
        },
        {
          path: "/login",
          name: "Login",
          component: () => import("@/views/Login.vue"),
        },
        {
          path: "/register",
          name: "Register",
          component: () => import("@/views/Register.vue"),
        },
        {
          path: "/page1",
          name: "page1",
          component: () => import("@/views/page1"),
        },
        {
          path: "/page2",
          name: "page2",
          component: () => import("@/views/page2"),
        },
        {
          path: "/page3",
          name: "page3",
          component: () => import("@/views/page3"),
        },
        {
          path: "/page4",
          name: "page4",
          component: () => import("@/views/page4"),
        },
      ],
    },
  ],
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  // 检查是否需要登录
  if (to.meta.requiresAuth && !token) {
    next("/login"); // 未登录，跳转到登录页面
  } else if (to.meta.role && to.meta.role !== role) {
    next("/"); // 无权限，跳转到首页
  } else {
    next(); // 放行
  }
});

export default router;
