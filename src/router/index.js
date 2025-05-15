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
      path: "/",
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
        {
          path: "/main_info",
          name: "main_info",
          component: () => import("@/views/main_info"),
        },
        {
          path: "/ig_center",
          name: "ig_center",
          component: () => import("@/views/ig_center"),
        },
      ],
    },
  ],
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      next("/login");
    } else if (to.meta.role && to.meta.role !== role) {
      next("/home/page1"); // 无权限时跳转到默认页
    } else {
      next();
    }
  } else {
    next(); // 不需要认证的路由直接放行
  }
});

export default router;
