import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    redirect: "/hrms/home",
  },
  {
    path: "/hrms/home",
    name: "Home",
    component: () => import("@/pages/Home.vue"),
    meta: { title: "Home", icon: "home" },
  },
  {
    path: "/hrms/checkin-logs",
    name: "CheckinLogs",
    component: () => import("@/pages/CheckinLogs.vue"),
    meta: { title: "Check-in Logs", icon: "clock" },
  },
  {
    path: "/hrms/leaves",
    name: "Leaves",
    component: () => import("@/pages/Leaves.vue"),
    meta: { title: "Leaves", icon: "calendar" },
  },
  {
    path: "/hrms/claims",
    name: "Claims",
    component: () => import("@/pages/Claims.vue"),
    meta: { title: "Claims", icon: "receipt" },
  },
  {
    path: "/hrms/salary",
    name: "Salary",
    component: () => import("@/pages/Salary.vue"),
    meta: { title: "Salary", icon: "dollar-sign" },
  },
  {
    path: "/hrms/profile",
    name: "Profile",
    component: () => import("@/pages/Profile.vue"),
    meta: { title: "Profile", icon: "user" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard for default date
router.beforeEach((to, from, next) => {
  // Set default date to today if not set
  if (!localStorage.getItem("selectedDate")) {
    localStorage.setItem(
      "selectedDate",
      new Date().toISOString().split("T")[0]
    );
  }
  next();
});

export default router;
