import frappe
from frappe import _


def after_install():
    create_custom_fields()
    create_dashboard()
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


def create_dashboard():
    if frappe.db.exists("Dashboard", "SLHRM"):
        frappe.delete_doc("Dashboard", "SLHRM")

    dash = frappe.get_doc({
        "doctype": "Dashboard",
        "name": "SLHRM",
        "dashboard_name": "SLHRM",
        "module": "SLHRM",
        "is_hidden": 0,
        "chart": [],
    })

    # Add number cards
    dash.append("number_cards", {
        "number_card": "Total Employees",
        "label": "Total Employees",
    })

    # Add charts
    dash.append("charts", {
        "chart_name": "Monthly Attendance Sheet",
        "label": "Attendance Overview",
    })

    dash.insert(ignore_permissions=True)
    print("  Created Dashboard: SLHRM")


def create_workspace():
    for doctype in ["Workspace Sidebar", "Workspace"]:
        existing = frappe.get_all(doctype, filters={"name": "SLHRM"})
        for doc in existing:
            frappe.delete_doc(doctype, doc.name, ignore_permissions=True)

    ws = frappe.get_doc({
        "doctype": "Workspace Sidebar",
        "name": "SLHRM",
        "title": "SLHRM",
        "label": "SLHRM",
        "header_icon": "hr",
        "app": "custom_hrms_pwa",
        "standard": 1,
        "public": 1,
        "items": _get_workspace_items(),
    })
    ws.insert(ignore_permissions=True)
    print("  Created Workspace: SLHRM")


def _get_workspace_items():
    items = []

    # ── Top-level navigation (not under any section) ──────────
    items.append(_top_link("Employee", "Employee", "DocType", "square-user-round"))

    # ── Setup Section ─────────────────────────────────────────
    items.append(_section("Setup", icon="database", keep_closed=True))
    items.append(_child_link("Company", "DocType", "building"))
    items.append(_child_link("Branch", "DocType", "git-branch"))
    items.append(_child_link("Department", "DocType", "list"))
    items.append(_child_link("Designation", "DocType", "tag"))
    items.append(_child_link("Employee Grade", "DocType", "award"))
    items.append(_child_link("Employee Group", "DocType", "users"))
    items.append(_child_link("Employment Type", "DocType", "briefcase"))
    items.append(_child_link("Holiday List", "DocType", "calendar"))

    # ── Attendance Section ────────────────────────────────────
    items.append(_section("Attendance", icon="clock"))
    items.append(_child_link("Employee Checkin", "DocType", "clipboard"))
    items.append(_child_link("Attendance", "DocType", "check-circle"))
    items.append(_child_link("Attendance Request", "DocType", "send"))
    items.append(_child_link("Biometric Punch Log", "DocType", "fingerprint"))
    items.append(_child_link("Attendance Marker", "DocType", "check-square"))
    items.append(_child_link("Shift Type", "DocType", "calendar"))
    items.append(_child_link("Shift Assignment", "DocType", "repeat"))
    items.append(_child_link("Shift Request", "DocType", "arrow-up"))

    # ── Leave Section ─────────────────────────────────────────
    items.append(_section("Leave", icon="book"))
    items.append(_child_link("Leave Type", "DocType", "tag"))
    items.append(_child_link("Leave Application", "DocType", "file-text"))
    items.append(_child_link("Leave Allocation", "DocType", "package"))
    items.append(_child_link("Leave Policy", "DocType", "shield"))
    items.append(_child_link("Leave Policy Assignment", "DocType", "shield"))
    items.append(_child_link("Leave Encashment", "DocType", "dollar-sign"))
    items.append(_child_link("Leave Block List", "DocType", "x-circle"))
    items.append(_child_link("Compensatory Leave Request", "DocType", "gift"))

    # ── Expense Section ───────────────────────────────────────
    items.append(_section("Expense", icon="credit-card"))
    items.append(_child_link("Expense Claim", "DocType", "credit-card"))
    items.append(_child_link("Expense Claim Type", "DocType", "layers"))
    items.append(_child_link("Employee Advance", "DocType", "bank"))

    # ── Payroll Section ───────────────────────────────────────
    items.append(_section("Payroll", icon="dollar-sign"))
    items.append(_child_link("Salary Slip", "DocType", "file-text"))
    items.append(_child_link("Salary Structure", "DocType", "briefcase"))
    items.append(_child_link("Salary Structure Assignment", "DocType", "briefcase"))
    items.append(_child_link("Payroll Entry", "DocType", "check-circle"))
    items.append(_child_link("Gratuity", "DocType", "star"))

    # ── Recruitment Section ───────────────────────────────────
    items.append(_section("Recruitment", icon="briefcase"))
    items.append(_child_link("Job Opening", "DocType", "briefcase"))
    items.append(_child_link("Job Applicant", "DocType", "user-plus"))
    items.append(_child_link("Interview", "DocType", "message-circle"))
    items.append(_child_link("Staffing Plan", "DocType", "users"))

    # ── Tools Section ─────────────────────────────────────────
    items.append(_section("Tools", icon="tool"))
    items.append(_child_link("Employee Attendance Tool", "DocType", "clipboard"))
    items.append(_child_link("Shift Assignment Tool", "DocType", "repeat"))
    items.append(_child_link("Leave Control Panel", "DocType", "settings"))

    # ── Reports Section (LAST) ────────────────────────────────
    items.append(_section("Reports", icon="file", keep_closed=True))
    items.append(_child_link("Monthly Attendance Sheet", "Report", "file"))
    items.append(_child_link("Employee Leave Balance Summary", "Report", "file"))
    items.append(_child_link("Leave Ledger", "Report", "file"))
    items.append(_child_link("Employee Advance Summary", "Report", "file"))
    items.append(_child_link("Unpaid Expense Claim", "Report", "file"))

    # ── Settings (very last) ──────────────────────────────────
    items.append(_section("Settings", icon="settings", keep_closed=True))
    items.append(_child_link("SLHRM Settings", "DocType", "setting"))
    items.append(_child_link("Custom Attendance Settings", "DocType", "setting"))
    items.append(_child_link("HR Settings", "DocType", "setting"))
    items.append(_child_link("Payroll Settings", "DocType", "setting"))

    return items


def _top_link(label, link_to, link_type, icon):
    """Top-level navigation link (not under any section)."""
    return {
        "type": "Link",
        "link_type": link_type,
        "link_to": link_to,
        "label": label,
        "icon": icon,
        "child": 0,
        "indent": 0,
        "collapsible": 0,
        "keep_closed": 0,
        "show_arrow": 0,
    }


def _section(label, icon=None, keep_closed=False):
    """Section Break with collapsible header."""
    return {
        "type": "Section Break",
        "label": label,
        "icon": icon or "circle",
        "child": 0,
        "indent": 1,
        "collapsible": 1,
        "keep_closed": 1 if keep_closed else 0,
        "show_arrow": 0,
    }


def _child_link(label, link_type, icon="link"):
    """Child link under a section."""
    return {
        "type": "Link",
        "link_type": link_type,
        "link_to": label,
        "label": label,
        "icon": icon,
        "child": 1,
        "indent": 0,
        "collapsible": 0,
        "keep_closed": 0,
        "show_arrow": 0,
    }
