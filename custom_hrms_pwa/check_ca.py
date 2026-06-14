import frappe

def execute():
    frappe.connect()

    for dt in ["Biometric Punch Log", "Attendance Marker", "Custom Attendance Settings"]:
        exists = frappe.db.exists("DocType", dt)
        print(f"  {dt}: {'YES' if exists else 'NO'}")

    # Check what custom_attendance has
    ca_dt = frappe.get_all("DocType", filters={"module": "Custom Attendance"}, pluck="name")
    print("\nCustom Attendance doctypes:", ca_dt)

    frappe.destroy()
