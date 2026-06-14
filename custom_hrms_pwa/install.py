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
        "items": _get_workspace_items(),
    })
    ws.insert(ignore_permissions=True)
    print("  Created Workspace: SLHRM")


def _get_workspace_items():
    """Build workspace items with proper Section Break + child Links."""
    items = []

    # ── Settings ──────────────────────────────────────────────
    items.append(_section("Settings", collapsible=False))
    items.append(_link("SLHRM Settings", "DocType", "setting"))

    # ── Employee ──────────────────────────────────────────────
    items.append(_section("Employee", icon="users"))
    items.append(_link("Employee", "DocType", "user"))
    items.append(_link("Designation", "DocType", "tag"))
    items.append(_link("Department", "DocType", "list"))
    items.append(_link("Branch", "DocType", "git-branch"))
    items.append(_link("Employee Grade", "DocType", "award"))
    items.append(_link("Holiday List", "DocType", "calendar"))

    # ── Attendance ────────────────────────────────────────────
    items.append(_section("Attendance", icon="clock"))
    items.append(_link("Employee Checkin", "DocType", "clipboard"))
    items.append(_link("Attendance", "DocType", "check-circle"))
    items.append(_link("Attendance Request", "DocType", "send"))
    items.append(_link("Shift Type", "DocType", "calendar"))
    items.append(_link("Shift Assignment", "DocType", "repeat"))
    items.append(_link("Shift Request", "DocType", "arrow-up"))

    # ── Leave ─────────────────────────────────────────────────
    items.append(_section("Leave", icon="book"))
    items.append(_link("Leave Type", "DocType", "tag"))
    items.append(_link("Leave Application", "DocType", "file-text"))
    items.append(_link("Leave Allocation", "DocType", "package"))
    items.append(_link("Leave Policy", "DocType", "shield"))
    items.append(_link("Leave Policy Assignment", "DocType", "shield"))
    items.append(_link("Leave Encashment", "DocType", "dollar-sign"))
    items.append(_link("Leave Block List", "DocType", "x-circle"))
    items.append(_link("Leave Control Panel", "DocType", "settings"))
    items.append(_link("Compensatory Leave Request", "DocType", "gift"))

    # ── Expense ───────────────────────────────────────────────
    items.append(_section("Expense", icon="credit-card"))
    items.append(_link("Expense Claim", "DocType", "credit-card"))
    items.append(_link("Expense Claim Type", "DocType", "layers"))
    items.append(_link("Employee Advance", "DocType", "bank"))

    # ── Payroll ───────────────────────────────────────────────
    items.append(_section("Payroll", icon="dollar-sign"))
    items.append(_link("Salary Slip", "DocType", "file-text"))
    items.append(_link("Salary Structure", "DocType", "briefcase"))
    items.append(_link("Salary Structure Assignment", "DocType", "briefcase"))
    items.append(_link("Payroll Entry", "DocType", "check-circle"))
    items.append(_link("Gratuity", "DocType", "star"))

    # ── Recruitment ───────────────────────────────────────────
    items.append(_section("Recruitment", icon="briefcase"))
    items.append(_link("Job Opening", "DocType", "briefcase"))
    items.append(_link("Job Applicant", "DocType", "user-plus"))
    items.append(_link("Interview", "DocType", "message-circle"))

    # ── Reports ───────────────────────────────────────────────
    items.append(_section("Reports", icon="file"))
    items.append(_link("Monthly Attendance Sheet", "Report", "file"))
    items.append(_link("Employee Leave Balance Summary", "Report", "file"))
    items.append(_link("Leave Ledger", "Report", "file"))

    return items


def _section(label, icon=None, collapsible=True):
    """Create a Section Break item (collapsible heading)."""
    item = {
        "type": "Section Break",
        "label": label,
        "collapsible": 1 if collapsible else 0,
    }
    if icon:
        item["icon"] = icon
    return item


def _link(label, link_type, icon="link"):
    """Create a Link item under the current section."""
    return {
        "type": "Link",
        "link_type": link_type,
        "link_to": label,
        "label": label,
        "icon": icon,
        "child": 1,
    }
