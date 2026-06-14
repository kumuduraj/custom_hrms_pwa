import frappe

def execute():
    frappe.connect()

    reports = frappe.get_all("Report", filters={"module": ["in", ["HR", "HRMS"]]}, pluck="name")
    print("HR Reports:", reports)

    for dt_name in ["Employee Benefit", "Gratuity", "Payment Entry", "Auto Attendance",
               "Leave Block List", "Leave Control Panel", "Salary Structure Assignment",
               "Bank Entry", "Employee Detail", "Leave Type", "Holiday List",
               "Attendance Request", "Shift Assignment", "Shift Request", "Shift Type",
               "Employee Advance", "Expense Claim Type"]:
        exists = frappe.db.exists("DocType", dt_name)
        print(f"  {dt_name}: {'YES' if exists else 'NO'}")

    frappe.destroy()
