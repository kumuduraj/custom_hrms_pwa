import frappe
from frappe import _


def after_install():
    create_custom_fields()
    create_workspace()
    frappe.db.commit()
    print("SLHRM: Installation complete.")


def after_uninstall():
    cfs = frappe.get_all("Custom Field", filters={"module": "SLHRM"})
    for cf in cfs:
        frappe.delete_doc("Custom Field", cf.name, ignore_permissions=True)

    wss = frappe.get_all("Workspace Sidebar", filters={"app": "custom_hrms_pwa"})
    for ws in wss:
        frappe.delete_doc("Workspace Sidebar", ws.name, ignore_permissions=True)

    frappe.db.commit()
    print("SLHRM: Uninstall complete.")


def create_custom_fields():
    fields_to_create = [
        {
            "dt": "Employee",
            "fieldname": "allow_mobile_checkin",
            "fieldtype": "Check",
            "label": "Allow Mobile Check-in",
            "default": "1",
            "insert_after": "column_break_45",
            "description": "Allow this employee to check in via SLHRM mobile app",
        }
    ]

    for field_def in fields_to_create:
        dt = field_def["dt"]
        fieldname = field_def["fieldname"]
        if frappe.db.exists("Custom Field", {"dt": dt, "fieldname": fieldname}):
            continue
        cf = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": dt,
            "fieldname": fieldname,
            "fieldtype": field_def.get("fieldtype", "Data"),
            "label": field_def.get("label"),
            "default": field_def.get("default"),
            "insert_after": field_def.get("insert_after"),
            "description": field_def.get("description"),
            "module": "SLHRM",
        })
        cf.insert(ignore_permissions=True)
        print(f"  Created Custom Field: {dt}-{fieldname}")


def create_workspace():
    # Delete any existing SLHRM workspace
    for doctype in ["Workspace Sidebar", "Workspace"]:
        existing = frappe.get_all(doctype, filters={"name": "SLHRM"})
        for doc in existing:
            frappe.delete_doc(doctype, doc.name, ignore_permissions=True)

    ws = frappe.get_doc({
        "doctype": "Workspace Sidebar",
        "name": "SLHRM",
        "label": "SLHRM",
        "title": "SLHRM",
        "header_icon": "hr",
        "app": "custom_hrms_pwa",
        "public": 1,
        "items": [
            # ── Settings ──────────────────────────────────────
            {"label": "SLHRM Settings", "link_to": "SLHRM Settings", "link_type": "DocType", "icon": "setting"},

            # ── Employee ──────────────────────────────────────
            {"label": "Employee", "link_to": "Employee", "link_type": "DocType", "icon": "users"},
            {"label": "Designation", "link_to": "Designation", "link_type": "DocType", "icon": "tag"},
            {"label": "Department", "link_to": "Department", "link_type": "DocType", "icon": "list"},
            {"label": "Branch", "link_to": "Branch", "link_type": "DocType", "icon": "git-branch"},
            {"label": "Grade", "link_to": "Employee Grade", "link_type": "DocType", "icon": "award"},
            {"label": "Holiday List", "link_to": "Holiday List", "link_type": "DocType", "icon": "calendar"},

            # ── Attendance ────────────────────────────────────
            {"label": "Employee Checkin", "link_to": "Employee Checkin", "link_type": "DocType", "icon": "clipboard"},
            {"label": "Attendance", "link_to": "Attendance", "link_type": "DocType", "icon": "check-circle"},
            {"label": "Attendance Request", "link_to": "Attendance Request", "link_type": "DocType", "icon": "clock"},
            {"label": "Shift Type", "link_to": "Shift Type", "link_type": "DocType", "icon": "calendar"},
            {"label": "Shift Assignment", "link_to": "Shift Assignment", "link_type": "DocType", "icon": "repeat"},
            {"label": "Shift Request", "link_to": "Shift Request", "link_type": "DocType", "icon": "send"},

            # ── Leave ─────────────────────────────────────────
            {"label": "Leave Type", "link_to": "Leave Type", "link_type": "DocType", "icon": "tag"},
            {"label": "Leave Application", "link_to": "Leave Application", "link_type": "DocType", "icon": "calendar"},
            {"label": "Leave Allocation", "link_to": "Leave Allocation", "link_type": "DocType", "icon": "package"},
            {"label": "Leave Policy", "link_to": "Leave Policy", "link_type": "DocType", "icon": "book"},
            {"label": "Leave Policy Assignment", "link_to": "Leave Policy Assignment", "link_type": "DocType", "icon": "book-open"},
            {"label": "Leave Encashment", "link_to": "Leave Encashment", "link_type": "DocType", "icon": "dollar-sign"},
            {"label": "Leave Block List", "link_to": "Leave Block List", "link_type": "DocType", "icon": "x-circle"},
            {"label": "Leave Control Panel", "link_to": "Leave Control Panel", "link_type": "DocType", "icon": "settings"},
            {"label": "Compensatory Leave Request", "link_to": "Compensatory Leave Request", "link_type": "DocType", "icon": "gift"},

            # ── Expense ───────────────────────────────────────
            {"label": "Expense Claim", "link_to": "Expense Claim", "link_type": "DocType", "icon": "credit-card"},
            {"label": "Expense Claim Type", "link_to": "Expense Claim Type", "link_type": "DocType", "icon": "layers"},
            {"label": "Employee Advance", "link_to": "Employee Advance", "link_type": "DocType", "icon": "bank"},

            # ── Payroll ───────────────────────────────────────
            {"label": "Salary Slip", "link_to": "Salary Slip", "link_type": "DocType", "icon": "file-text"},
            {"label": "Salary Structure", "link_to": "Salary Structure", "link_type": "DocType", "icon": "briefcase"},
            {"label": "Salary Structure Assignment", "link_to": "Salary Structure Assignment", "link_type": "DocType", "icon": "briefcase"},
            {"label": "Payroll Entry", "link_to": "Payroll Entry", "link_type": "DocType", "icon": "dollar-sign"},
            {"label": "Gratuity", "link_to": "Gratuity", "link_type": "DocType", "icon": "star"},

            # ── Recruitment ───────────────────────────────────
            {"label": "Job Opening", "link_to": "Job Opening", "link_type": "DocType", "icon": "briefcase"},
            {"label": "Job Applicant", "link_to": "Job Applicant", "link_type": "DocType", "icon": "user-plus"},
            {"label": "Interview", "link_to": "Interview", "link_type": "DocType", "icon": "message-circle"},

            # ── Reports ───────────────────────────────────────
            {"label": "Monthly Attendance Sheet", "link_to": "Monthly Attendance Sheet", "link_type": "Report", "icon": "file"},
            {"label": "Employee Leave Balance", "link_to": "Employee Leave Balance Summary", "link_type": "Report", "icon": "file"},
            {"label": "Leave Ledger", "link_to": "Leave Ledger", "link_type": "Report", "icon": "file"},
        ],
    })
    ws.insert(ignore_permissions=True)
    print("  Created Workspace: SLHRM")
