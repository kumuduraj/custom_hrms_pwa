<template>
  <div class="checkin-logs-page">
    <div class="page-header">
      <h1>Check-in Logs</h1>
      <div class="date-picker">
        <input type="date" v-model="selectedDate" @change="fetchLogs" />
      </div>
    </div>

    <div class="employee-list" v-if="employees.length">
      <div
        class="employee-card"
        v-for="emp in employees"
        :key="emp.employee"
        @click="toggleExpand(emp.employee)"
      >
        <div class="employee-info">
          <div class="employee-name">{{ emp.employee_name }}</div>
          <div class="employee-id">{{ emp.employee }}</div>
        </div>
        <div class="employee-summary">
          <div class="time-info" v-if="emp.in_time">
            <span class="label">IN:</span>
            <span class="value">{{ formatTime(emp.in_time) }}</span>
          </div>
          <div class="time-info" v-if="emp.out_time">
            <span class="label">OUT:</span>
            <span class="value">{{ formatTime(emp.out_time) }}</span>
          </div>
          <div class="worked-hours" v-if="emp.worked_hours">
            {{ emp.worked_hours }}h
          </div>
        </div>
        <div class="expand-icon" :class="{ expanded: expanded[emp.employee] }">
          ▼
        </div>
      </div>
    </div>

    <div class="empty-state" v-else>
      <div class="icon">📋</div>
      <p>No check-in logs found for this date</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { call } from "frappe-ui";

const selectedDate = ref(new Date().toISOString().split("T")[0]);
const employees = ref([]);
const expanded = ref({});

const fetchLogs = async () => {
  try {
    const response = await call(
      "custom_hrms_pwa.api.get_supervisor_checkin_logs",
      { date: selectedDate.value }
    );
    employees.value = response.employees || [];
  } catch (error) {
    console.error("Failed to fetch logs:", error);
    employees.value = [];
  }
};

const toggleExpand = (employee) => {
  expanded.value[employee] = !expanded.value[employee];
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
  fetchLogs();
});
</script>

<style scoped>
.checkin-logs-page {
  padding: 16px;
  max-width: 600px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.date-picker input {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
}

.employee-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.employee-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.employee-card:hover {
  border-color: #3b82f6;
}

.employee-info {
  margin-bottom: 8px;
}

.employee-name {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.employee-id {
  font-size: 12px;
  color: #6b7280;
}

.employee-summary {
  display: flex;
  gap: 16px;
  align-items: center;
}

.time-info {
  font-size: 14px;
}

.time-info .label {
  color: #6b7280;
  margin-right: 4px;
}

.time-info .value {
  color: #1f2937;
  font-weight: 500;
}

.worked-hours {
  background: #dbeafe;
  color: #1d4ed8;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.expand-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  transition: transform 0.2s;
  color: #9ca3af;
}

.expand-icon.expanded {
  transform: translateY(-50%) rotate(180deg);
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.empty-state .icon {
  font-size: 48px;
  margin-bottom: 16px;
}
</style>
