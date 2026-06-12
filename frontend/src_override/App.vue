<template>
  <div class="app-container">
    <router-view />
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from "@/components/BottomNav.vue";
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
    Ubuntu, Cantarell, sans-serif;
  background: #f9fafb;
  color: #1f2937;
}

.app-container {
  min-height: 100vh;
  padding-bottom: 70px;
}
</style>
