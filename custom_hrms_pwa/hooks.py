app_name = "custom_hrms_pwa"
app_title = "SLHRM"
app_publisher = "Rajitha"
app_description = "Custom HRMS Mobile App - SLHRM"
app_version = "0.0.1"
app_color = "#3b82f6"
app_icon = "octicon octicon-clock"
app_email = "rajclost@gmail.com"
app_license = "mit"

app_logo_url = "/assets/custom_hrms_pwa/images/logo-192.png"

# Installation
after_install = "custom_hrms_pwa.install.after_install"
after_uninstall = "custom_hrms_pwa.install.after_uninstall"

# Fixtures - export custom fields and property setters
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Custom HRMS PWA"]],
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "Custom HRMS PWA"]],
    },
]

# Website route rules
website_route_rules = [
    {"from_route": "/slhrms", "to_route": "slhrms"},
    {"from_route": "/slhrms/<path:app_path>", "to_route": "slhrms"},
]
