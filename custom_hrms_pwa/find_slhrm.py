import frappe

def execute():
    frappe.connect()

    # Find ALL SLHRM related entries
    for dt in ["Workspace Sidebar", "Workspace", "Module Def", "Desktop Icon", "Has Role"]:
        results = frappe.get_all(dt, filters={"name": ["like", "%SLHRM%"]}, pluck="name")
        if results:
            print(f"{dt}: {results}")

    # Also check by label
    for dt in ["Workspace Sidebar", "Workspace", "Module Def"]:
        results = frappe.get_all(dt, filters={"label": ["like", "%SLHRM%"]}, pluck="name")
        if results:
            print(f"{dt} (by label): {results}")

    # Check module def
    md = frappe.get_all("Module Def", filters={"name": "SLHRM"}, pluck="name")
    print(f"Module Def SLHRM: {md}")

    # Check workspace
    ws = frappe.get_all("Workspace", filters={"name": "SLHRM"}, pluck="name")
    print(f"Workspace SLHRM: {ws}")

    # Check sidebar
    sb = frappe.get_all("Workspace Sidebar", filters={"name": "SLHRM"}, pluck="name")
    print(f"Sidebar SLHRM: {sb}")

    frappe.destroy()
