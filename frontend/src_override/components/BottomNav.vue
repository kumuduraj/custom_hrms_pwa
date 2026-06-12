<template>
  <nav class="bottom-nav">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="nav-item"
      :class="{ active: isActive(item.path) }"
    >
      <div class="nav-icon">{{ item.icon }}</div>
      <div class="nav-label">{{ item.label }}</div>
    </router-link>
  </nav>
</template>

<script setup>
import { useRoute } from "vue-router";

const route = useRoute();

const navItems = [
  { path: "/hrms/home", label: "Home", icon: "🏠" },
  { path: "/hrms/checkin-logs", label: "Check-ins", icon: "📋" },
  { path: "/hrms/leaves", label: "Leaves", icon: "📅" },
  { path: "/hrms/salary", label: "Salary", icon: "💵" },
  { path: "/hrms/profile", label: "Profile", icon: "👤" },
];

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + "/");
};
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  z-index: 100;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #6b7280;
  padding: 4px 12px;
  transition: color 0.2s;
}

.nav-item.active {
  color: #3b82f6;
}

.nav-icon {
  font-size: 20px;
  margin-bottom: 2px;
}

.nav-label {
  font-size: 10px;
  font-weight: 500;
}
</style>
