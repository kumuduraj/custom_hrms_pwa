import frappe

def execute():
    frappe.connect()
    dashboards = frappe.get_all("Dashboard", pluck="name")
    print("Existing Dashboards:", dashboards)
    frappe.destroy()
