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
    if frappe.db.exists("Workspace Sidebar", {"name": "SLHRM", "app": "custom_hrms_pwa"}):
        # Fix header_icon if missing
        frappe.db.set_value("Workspace Sidebar", "SLHRM", "header_icon", "hr")
        print("  Workspace SLHRM already exists (fixed header_icon)")
        return

    ws = frappe.get_doc({
        "doctype": "Workspace Sidebar",
        "name": "SLHRM",
        "label": "SLHRM",
        "title": "SLHRM",
        "header_icon": "hr",
        "app": "custom_hrms_pwa",
        "public": 1,
        "items": [
            {"label": "SLHRM Settings", "link_to": "SLHRM Settings", "link_type": "DocType", "icon": "setting"},
            {"label": "Employee", "link_to": "Employee", "link_type": "DocType", "icon": "users"},
            {"label": "Employee Checkin", "link_to": "Employee Checkin", "link_type": "DocType", "icon": "clipboard"},
            {"label": "Leave Application", "link_to": "Leave Application", "link_type": "DocType", "icon": "calendar"},
            {"label": "Expense Claim", "link_to": "Expense Claim", "link_type": "DocType", "icon": "credit-card"},
            {"label": "Salary Slip", "link_to": "Salary Slip", "link_type": "DocType", "icon": "money"},
        ],
    })
    ws.insert(ignore_permissions=True)
    print("  Created Workspace: SLHRM")
