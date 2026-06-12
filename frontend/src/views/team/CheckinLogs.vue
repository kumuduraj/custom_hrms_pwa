<template>
	<BaseLayout :pageTitle="__('Team Check-ins')">
		<template #body>
			<div class="flex flex-col mt-4 mb-7 p-4 gap-4">
				<!-- Date Picker -->
				<div class="flex items-center gap-3">
					<Button
						variant="subtle"
						@click="prevDay"
						class="!py-1 !px-2"
					>
						<FeatherIcon name="chevron-left" class="h-4 w-4" />
					</Button>
					<div class="flex-1 text-center">
						<input
							type="date"
							v-model="selectedDate"
							class="w-full text-center text-sm font-medium text-gray-800 border-0 bg-transparent focus:outline-none cursor-pointer"
							@change="fetchLogs"
						/>
					</div>
					<Button
						variant="subtle"
						@click="nextDay"
						class="!py-1 !px-2"
					>
						<FeatherIcon name="chevron-right" class="h-4 w-4" />
					</Button>
					<Button
						variant="subtle"
						@click="goToday"
						class="!py-1 !px-3 text-xs"
					>
						{{ __("Today") }}
					</Button>
				</div>

				<!-- Loading -->
				<div v-if="logs.loading" class="flex justify-center py-8">
					<Spinner class="h-6 w-6" />
				</div>

				<!-- Empty State -->
				<div
					v-else-if="!logs.data?.employees?.length"
					class="flex flex-col items-center py-12 text-center"
				>
					<FeatherIcon name="users" class="h-12 w-12 text-gray-300 mb-3" />
					<div class="text-gray-500 text-sm">
						{{ __("No team check-ins found for this date") }}
					</div>
					<div class="text-gray-400 text-xs mt-1">
						{{ __("Employees under your supervision will appear here") }}
					</div>
				</div>

				<!-- Employee Cards -->
				<div v-else class="flex flex-col gap-3">
					<div class="text-sm text-gray-500 font-medium">
						{{ logs.data.employees.length }} {{ __("employee(s)") }}
					</div>

					<div
						v-for="emp in logs.data.employees"
						:key="emp.employee"
						class="bg-white rounded-lg border border-gray-200 p-4"
					>
						<!-- Employee Header -->
						<div class="flex items-center justify-between mb-3">
							<div class="flex items-center gap-2">
								<Avatar :label="emp.employee_name" size="sm" />
								<div>
									<div class="text-sm font-semibold text-gray-800">
										{{ emp.employee_name }}
									</div>
									<div class="text-xs text-gray-500">
										{{ emp.employee }}
									</div>
								</div>
							</div>
							<div
								class="text-xs px-2 py-1 rounded-full"
								:class="getStatusClass(emp)"
							>
								{{ getStatusLabel(emp) }}
							</div>
						</div>

						<!-- Summary Row -->
						<div class="grid grid-cols-3 gap-2 text-center mb-3">
							<div class="bg-gray-50 rounded p-2">
								<div class="text-xs text-gray-500">{{ __("In") }}</div>
								<div class="text-sm font-medium text-gray-800">
									{{ formatTime(emp.in_time) }}
								</div>
							</div>
							<div class="bg-gray-50 rounded p-2">
								<div class="text-xs text-gray-500">{{ __("Out") }}</div>
								<div class="text-sm font-medium text-gray-800">
									{{ formatTime(emp.out_time) }}
								</div>
							</div>
							<div class="bg-gray-50 rounded p-2">
								<div class="text-xs text-gray-500">{{ __("Hours") }}</div>
								<div class="text-sm font-medium text-gray-800">
									{{ emp.worked_hours ? emp.worked_hours + "h" : "--" }}
								</div>
							</div>
						</div>

						<!-- Punch Details -->
						<div v-if="emp.checkins?.length" class="border-t pt-2">
							<div
								v-for="checkin in emp.checkins"
								:key="checkin.name"
								class="flex items-center justify-between py-1 text-xs"
							>
								<div class="flex items-center gap-2">
									<span
										class="inline-block w-2 h-2 rounded-full"
										:class="
											checkin.log_type === 'IN'
												? 'bg-green-500'
												: 'bg-red-500'
										"
									></span>
									<span class="text-gray-600">{{ checkin.log_type }}</span>
									<span
										v-if="checkin.latitude && checkin.longitude"
										class="text-blue-500 ml-1 cursor-pointer"
										:title="getLocationText(checkin)"
									>
										<FeatherIcon name="map-pin" class="h-3 w-3" />
									</span>
								</div>
								<div class="flex items-center gap-2">
									<span class="text-gray-800 font-medium">
										{{ formatTime(checkin.time) }}
									</span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</template>
	</BaseLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { FeatherIcon, Button, Avatar, Spinner } from "frappe-ui"
import BaseLayout from "@/components/BaseLayout.vue"
import { teamCheckinLogs, formatTime } from "@/data/team"
import dayjs from "@/utils/dayjs"

const selectedDate = ref(dayjs().format("YYYY-MM-DD"))
const logs = teamCheckinLogs

const fetchLogs = () => {
	logs.fetch({
		date: selectedDate.value,
	})
}

const prevDay = () => {
	selectedDate.value = dayjs(selectedDate.value).subtract(1, "day").format("YYYY-MM-DD")
	fetchLogs()
}

const nextDay = () => {
	selectedDate.value = dayjs(selectedDate.value).add(1, "day").format("YYYY-MM-DD")
	fetchLogs()
}

const goToday = () => {
	selectedDate.value = dayjs().format("YYYY-MM-DD")
	fetchLogs()
}

const getStatusClass = (emp) => {
	if (!emp.in_time) return "bg-gray-100 text-gray-500"
	if (!emp.out_time) return "bg-green-100 text-green-700"
	return "bg-blue-100 text-blue-700"
}

const getStatusLabel = (emp) => {
	if (!emp.in_time) return "No check-in"
	if (!emp.out_time) return "Checked in"
	return "Checked out"
}

const getLocationText = (checkin) => {
	if (checkin.latitude && checkin.longitude) {
		return `${checkin.latitude.toFixed(6)}, ${checkin.longitude.toFixed(6)}`
	}
	return ""
}

onMounted(() => {
	fetchLogs()
})
</script>
