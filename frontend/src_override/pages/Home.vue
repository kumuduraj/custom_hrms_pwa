<template>
  <div class="home-page">
    <div class="welcome-section">
      <h1>Welcome, {{ userName }}</h1>
      <p class="date">{{ formattedDate }}</p>
    </div>

    <div class="checkin-panel">
      <div class="status-card" :class="statusClass">
        <div class="status-icon">
          {{ isCheckedIn ? "✓" : "⏰" }}
        </div>
        <div class="status-text">
          {{ isCheckedIn ? "Checked In" : "Not Checked In" }}
        </div>
        <div class="time" v-if="summary.in_time">
          {{ formatTime(summary.in_time) }}
        </div>
      </div>

      <div class="summary-row" v-if="summary.in_time">
        <div class="summary-item">
          <span class="label">Check In</span>
          <span class="value">{{ formatTime(summary.in_time) }}</span>
        </div>
        <div class="summary-item">
          <span class="label">Check Out</span>
          <span class="value">{{ summary.out_time ? formatTime(summary.out_time) : "--" }}</span>
        </div>
        <div class="summary-item">
          <span class="label">Worked</span>
          <span class="value">{{ summary.worked_hours || 0 }}h</span>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>Quick Actions</h2>
      <div class="action-grid">
        <router-link to="/hrms/checkin-logs" class="action-card">
          <div class="action-icon">📋</div>
          <div class="action-label">Check-in Logs</div>
        </router-link>
        <router-link to="/hrms/leaves" class="action-card">
          <div class="action-icon">📅</div>
          <div class="action-label">Leaves</div>
        </router-link>
        <router-link to="/hrms/claims" class="action-card">
          <div class="action-icon">💰</div>
          <div class="action-label">Claims</div>
        </router-link>
        <router-link to="/hrms/salary" class="action-card">
          <div class="action-icon">💵</div>
          <div class="action-label">Salary</div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { call } from "frappe-ui";

const userName = ref("");
const summary = ref({});
const selectedDate = ref(new Date().toISOString().split("T")[0]);

const formattedDate = computed(() => {
  const date = new Date(selectedDate.value);
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
});

const isCheckedIn = computed(() => {
  return summary.value.in_time && !summary.value.out_time;
});

const statusClass = computed(() => ({
  "checked-in": isCheckedIn.value,
  "checked-out": summary.value.out_time,
  "not-started": !summary.value.in_time,
}));

const fetchSummary = async () => {
  try {
    const response = await call(
      "custom_hrms_pwa.api.get_employee_checkin_summary",
      { date: selectedDate.value }
    );
    summary.value = response || {};
  } catch (error) {
    console.error("Failed to fetch summary:", error);
  }
};

const fetchUserInfo = async () => {
  try {
    const user = await call("frappe.client.get_value", {
      doctype: "User",
      filters: { name: frappe.session.user },
      fieldname: "full_name",
    });
    userName.value = user.full_name || frappe.session.user;
  } catch (error) {
    userName.value = frappe.session.user;
  }
};

const formatTime = (time) => {
  if (!time) return "";
  const date = new Date(time);
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
};

onMounted(() => {
  fetchUserInfo();
  fetchSummary();
});
</script>

<style scoped>
.home-page {
  padding: 16px;
  max-width: 600px;
  margin: 0 auto;
}

.welcome-section {
  margin-bottom: 24px;
}

.welcome-section h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
  color: #1f2937;
}

.welcome-section .date {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.checkin-panel {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 24px;
}

.status-card {
  text-align: center;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 16px;
}

.status-card.checked-in {
  background: #dcfce7;
  color: #166534;
}

.status-card.checked-out {
  background: #dbeafe;
  color: #1e40af;
}

.status-card.not-started {
  background: #fef3c7;
  color: #92400e;
}

.status-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.status-text {
  font-size: 18px;
  font-weight: 600;
}

.time {
  font-size: 14px;
  margin-top: 4px;
}

.summary-row {
  display: flex;
  justify-content: space-around;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.summary-item {
  text-align: center;
}

.summary-item .label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.summary-item .value {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.quick-actions h2 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #1f2937;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
}

.action-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.action-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.action-label {
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}
</style>
