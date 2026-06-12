app_name = "custom_hrms_pwa"
app_title = "SLHRM"
app_publisher = "Rajitha"
app_description = "Custom HRMS Mobile App - SLHRM"
app_version = "0.0.1"
app_color = "#3b82f6"
app_icon = "octicon octicon-clock"
app_email = "rajclost@gmail.com"
app_license = "mit"
required_apps = ["frappe/erpnext", "frappe/hrms"]

app_logo_url = "/assets/custom_hrms_pwa/images/logo-192.png"

add_to_apps_screen = [
    {
        "name": "custom_hrms_pwa",
        "logo": "/assets/custom_hrms_pwa/images/logo-192.png",
        "title": "SLHRM",
        "route": "/hrms/home",
        "has_permission": "custom_hrms_pwa.api.check_app_permission",
    }
]

app_include_js = "/assets/custom_hrms_pwa/js/custom_hrms_pwa.js"
app_include_css = "/assets/custom_hrms_pwa/css/custom_hrms_pwa.css"

boot_session = "custom_hrms_pwa.api.boot_session"
