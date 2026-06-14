import { createApp } from "vue";
import { createPinia } from "pinia";
import { setConfig, frappeRequest, resourcesPlugin } from "frappe-ui";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);
const pinia = createPinia();

setConfig("resourceFetcher", frappeRequest);
app.use(resourcesPlugin);
app.use(pinia);
app.use(router);

app.mount("#app");
