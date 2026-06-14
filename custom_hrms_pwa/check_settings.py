import frappe

def execute():
    frappe.connect()

    # Find all Settings-related doctypes in HR/HRMS modules
    settings = frappe.get_all("DocType", 
        filters={"module": ["in", ["HR", "HRMS", "Setup"]], "issingle": 1},
        fields=["name", "module"],
        order_by="name"
    )
    print("Single (Settings) Doctypes:")
    for s in settings:
        print(f"  {s.name} ({s.module})")

    # Also check common setup doctypes
    print("\nOther relevant doctypes:")
    for dt in ["HR Settings", "Payroll Settings", "Company", "Branch", "Department", 
               "Designation", "Employee Grade", "Employee Group", "Employment Type",
               "Staffing Plan", "Job Opening", "Job Applicant", "Interview",
               "Leave Type", "Leave Policy", "Holiday List", "Attendance",
               "Shift Type", "Salary Structure", "Payroll Entry"]:
        exists = frappe.db.exists("DocType", dt)
        print(f"  {dt}: {'YES' if exists else 'NO'}")

    frappe.destroy()
