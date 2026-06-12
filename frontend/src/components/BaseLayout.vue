<template>
	<ion-page>
		<ion-header class="ion-no-border">
			<div class="w-full sm:w-96">
				<div class="flex flex-col bg-white shadow-sm p-4">
					<div class="flex flex-row justify-between items-center">
						<div class="flex flex-row items-center gap-2">
							<img
								v-if="companyLogo"
								:src="companyLogo"
								alt="Logo"
								class="h-8 w-8 object-contain rounded"
							/>
							<h2 class="text-xl font-bold text-gray-900">
								{{ props.pageTitle || __("SLHRM") }}
							</h2>
						</div>
						<div class="flex flex-row items-center gap-3 ml-auto">
							<router-link
								:to="{ name: 'Notifications' }"
								v-slot="{ navigate }"
								class="flex flex-col items-center"
							>
								<span class="relative inline-block" @click="navigate">
									<FeatherIcon name="bell" class="h-6 w-6" />
									<span
										v-if="unreadNotificationsCount.data"
										class="absolute top-0 right-0.5 inline-block w-2 h-2 bg-red-600 rounded-full border border-white"
									>
									</span>
								</span>
							</router-link>
							<router-link
								:to="{ name: 'Profile' }"
								class="flex flex-col items-center"
							>
								<Avatar
									:image="user.data.user_image"
									:label="user.data.first_name"
									size="xl"
								/>
							</router-link>
						</div>
					</div>
				</div>
			</div>
		</ion-header>

		<ion-content class="ion-no-padding">
			<div class="flex flex-col h-screen w-screen sm:w-96">
				<slot name="body"></slot>
			</div>
		</ion-content>
	</ion-page>
</template>

<script setup>
import { IonHeader, IonContent, IonPage } from "@ionic/vue"
import { FeatherIcon, Avatar, call } from "frappe-ui"
import { ref, onMounted } from "vue"

import { unreadNotificationsCount } from "@/data/notifications"

import { inject } from "vue"

const user = inject("$user")

const companyLogo = ref(null)

const props = defineProps({
	pageTitle: {
		type: String,
		required: false,
		default: "",
	},
})

onMounted(async () => {
	try {
		const res = await call("custom_hrms_pwa.api.get_company_logo")
		if (res && res.logo_url) {
			companyLogo.value = res.logo_url
		}
	} catch (e) {
		// ignore - no logo available
	}
})
</script>
