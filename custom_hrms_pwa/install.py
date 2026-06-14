import frappe
from frappe import _


def after_install():
    """Run after bench --site install-app custom_hrms_pwa."""
    create_custom_fields()
    create_workspace()
    frappe.db.commit()
    print("SLHRM: Installation complete.")


def create_custom_fields():
    """Create custom fields needed by SLHRM."""
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
            print(f"  Custom Field already exists: {dt}-{fieldname}")
            continue

        cf = frappe.get_doc(
            {
                "doctype": "Custom Field",
                "dt": dt,
                "fieldname": fieldname,
                "fieldtype": field_def.get("fieldtype", "Data"),
                "label": field_def.get("label"),
                "default": field_def.get("default"),
                "insert_after": field_def.get("insert_after"),
                "description": field_def.get("description"),
                "module": "Custom HRMS PWA",
            }
        )
        cf.insert(ignore_permissions=True)
        print(f"  Created Custom Field: {dt}-{fieldname}")


def create_workspace():
    """Create SLHRM workspace sidebar."""
    if frappe.db.exists("Workspace Sidebar", "SLHRM"):
        print("  Workspace SLHRM already exists")
        return

    ws = frappe.get_doc(
        {
            "doctype": "Workspace Sidebar",
            "name": "SLHRM",
            "label": "SLHRM",
            "title": "SLHRM",
            "app": "custom_hrms_pwa",
            "public": 1,
            "items": [
                {
                    "label": "SLHRM Settings",
                    "link_to": "SLHRM Settings",
                    "link_type": "DocType",
                    "icon": "setting",
                },
                {
                    "label": "Employee",
                    "link_to": "Employee",
                    "link_type": "DocType",
                    "icon": "users",
                },
                {
                    "label": "Employee Checkin",
                    "link_to": "Employee Checkin",
                    "link_type": "DocType",
                    "icon": "clipboard",
                },
                {
                    "label": "Leave Application",
                    "link_to": "Leave Application",
                    "link_type": "DocType",
                    "icon": "calendar",
                },
                {
                    "label": "Expense Claim",
                    "link_to": "Expense Claim",
                    "link_type": "DocType",
                    "icon": "credit-card",
                },
                {
                    "label": "Salary Slip",
                    "link_to": "Salary Slip",
                    "link_type": "DocType",
                    "icon": "money",
                },
            ],
        }
    )
    ws.insert(ignore_permissions=True)
    print("  Created Workspace: SLHRM")
