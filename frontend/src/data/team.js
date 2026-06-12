import { createResource } from "frappe-ui"
import dayjs from "@/utils/dayjs"

export const teamCheckinLogs = createResource({
	url: "custom_hrms_pwa.api.get_supervisor_checkin_logs",
	method: "GET",
	makeParams(params) {
		return {
			date: params.date || dayjs().format("YYYY-MM-DD"),
			employee: params.employee || undefined,
		}
	},
	transform(data) {
		return data
	},
})

export const formatTime = (time) => {
	if (!time) return "--"
	return dayjs(time).format("hh:mm A")
}

export const formatDate = (date) => {
	return dayjs(date).format("D MMM YYYY")
}
