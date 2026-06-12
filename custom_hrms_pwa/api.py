import frappe
from frappe import _
from datetime import datetime, timedelta


def boot_session(bootinfo):
    """Add custom info to boot session."""
    bootinfo.app_name = "SLHRM"
    bootinfo.app_logo_url = "/assets/custom_hrms_pwa/images/logo-192.png"

    defaults = frappe.defaults.get_defaults()
    company = defaults.get("company")
    if company:
        # Prefer PWA Logo, fallback to company_logo
        pwa_logo = frappe.db.get_value("Company", company, "pwa_logo")
        company_logo = frappe.db.get_value("Company", company, "company_logo")
        logo = pwa_logo or company_logo
        if logo:
            if logo.startswith("http"):
                bootinfo.company_logo_url = logo
            elif logo.startswith("/files/"):
                bootinfo.company_logo_url = logo
            else:
                bootinfo.company_logo_url = f"/files/{logo}"
        bootinfo.company_name = company

    # Check mobile checkin permission for current employee
    user = frappe.session.user
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if employee:
        allow_mobile = frappe.db.get_value("Employee", employee, "allow_mobile_checkin")
        bootinfo.allow_mobile_checkin = bool(allow_mobile) if allow_mobile is not None else True
    else:
        bootinfo.allow_mobile_checkin = False


@frappe.whitelist()
def check_app_permission():
    """Check if user has permission to access the app."""
    user = frappe.session.user
    # Allow access to System Manager, HR Manager, HR User
    roles = frappe.get_roles(user)
    if any(r in roles for r in ["System Manager", "HR Manager", "HR User"]):
        return True
    # Allow if user has an Employee record
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    return bool(employee)


@frappe.whitelist()
def check_mobile_checkin_permission():
    """Check if current employee is allowed to check in via mobile."""
    user = frappe.session.user
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not employee:
        return {"allowed": False, "reason": "No employee record found"}

    allow_mobile = frappe.db.get_value("Employee", employee, "allow_mobile_checkin")
    if not allow_mobile:
        return {"allowed": False, "reason": "Mobile check-in not enabled for this employee"}

    return {"allowed": True, "employee": employee}


@frappe.whitelist()
def get_supervisor_checkin_logs(date=None, employee=None):
    """
    Get check-in logs for employees under current user's supervision.
    Used in the PWA Check-in Logs tab.
    """
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    user = frappe.session.user

    # Get employees supervised by current user
    supervised_employees = get_supervised_employees(user)

    if not supervised_employees:
        return {"employees": [], "logs": []}

    # If specific employee requested, filter to that one
    if employee and employee in supervised_employees:
        supervised_employees = [employee]

    # Get check-in logs for the date
    logs = frappe.get_all(
        "Employee Checkin",
        filters={
            "employee": ["in", supervised_employees],
            "time": ["between", [f"{date} 00:00:00", f"{date} 23:59:59"]],
        },
        fields=[
            "name",
            "employee",
            "employee_name",
            "time",
            "log_type",
            "device_id",
            "skip_auto_attendance",
            "latitude",
            "longitude",
        ],
        order_by="employee asc, time asc",
    )

    # Group logs by employee
    employee_logs = {}
    for log in logs:
        emp = log.employee
        if emp not in employee_logs:
            employee_logs[emp] = {
                "employee": emp,
                "employee_name": log.employee_name,
                "checkins": [],
            }
        employee_logs[emp]["checkins"].append(
            {
                "name": log.name,
                "time": log.time,
                "log_type": log.log_type,
                "device_id": log.device_id,
                "latitude": log.latitude,
                "longitude": log.longitude,
            }
        )

    # Calculate summary for each employee
    employees = []
    for emp_name, emp_data in employee_logs.items():
        checkins = emp_data["checkins"]
        in_time = None
        out_time = None
        worked_hours = 0

        for c in checkins:
            if c["log_type"] == "IN" and not in_time:
                in_time = c["time"]
            if c["log_type"] == "OUT":
                out_time = c["time"]

        if in_time and out_time:
            in_dt = (
                in_time
                if isinstance(in_time, datetime)
                else datetime.strptime(str(in_time), "%Y-%m-%d %H:%M:%S")
            )
            out_dt = (
                out_time
                if isinstance(out_time, datetime)
                else datetime.strptime(str(out_time), "%Y-%m-%d %H:%M:%S")
            )
            worked_hours = round((out_dt - in_dt).total_seconds() / 3600, 2)

        employees.append(
            {
                "employee": emp_name,
                "employee_name": emp_data["employee_name"],
                "in_time": in_time,
                "out_time": out_time,
                "worked_hours": worked_hours,
                "total_punches": len(checkins),
                "checkins": checkins,
            }
        )

    return {
        "date": date,
        "supervisor": user,
        "employees": employees,
    }


def get_supervised_employees(user):
    """Get list of employee names supervised by the given user."""
    # Check if user is an Employee
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not employee:
        return []

    # Get employees where reports_to = current employee
    supervised = frappe.get_all(
        "Employee",
        filters={"reports_to": employee, "status": "Active"},
        fields=["name"],
    )

    # If no direct reports, check if user is HR Manager/HR User
    if not supervised:
        roles = frappe.get_roles(user)
        if any(r in roles for r in ["System Manager", "HR Manager"]):
            # HR Managers see all active employees
            all_emp = frappe.get_all(
                "Employee",
                filters={"status": "Active"},
                fields=["name"],
            )
            return [e.name for e in all_emp]

    return [e.name for e in supervised]


@frappe.whitelist()
def get_company_logo():
    """Get company logo for PWA branding."""
    defaults = frappe.defaults.get_defaults()
    company = defaults.get("company")
    if not company:
        return {"logo_url": None, "company_name": None}

    # Prefer PWA Logo, fallback to company_logo
    pwa_logo = frappe.db.get_value("Company", company, "pwa_logo")
    company_logo = frappe.db.get_value("Company", company, "company_logo")
    logo = pwa_logo or company_logo

    logo_url = None
    if logo:
        if logo.startswith("http"):
            logo_url = logo
        elif logo.startswith("/files/"):
            logo_url = logo
        else:
            logo_url = f"/files/{logo}"

    return {"logo_url": logo_url, "company_name": company}


@frappe.whitelist()
def get_employee_checkin_summary(date=None):
    """Get check-in summary for current employee (for home page)."""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    user = frappe.session.user
    employee = frappe.db.get_value("Employee", {"user_id": user}, "name")
    if not employee:
        return {}

    logs = frappe.get_all(
        "Employee Checkin",
        filters={
            "employee": employee,
            "time": ["between", [f"{date} 00:00:00", f"{date} 23:59:59"]],
        },
        fields=["time", "log_type", "device_id"],
        order_by="time asc",
    )

    in_time = None
    out_time = None
    for log in logs:
        if log.log_type == "IN" and not in_time:
            in_time = log.time
        if log.log_type == "OUT":
            out_time = log.time

    worked_hours = 0
    if in_time and out_time:
        in_dt = (
            in_time
            if isinstance(in_time, datetime)
            else datetime.strptime(str(in_time), "%Y-%m-%d %H:%M:%S")
        )
        out_dt = (
            out_time
            if isinstance(out_time, datetime)
            else datetime.strptime(str(out_time), "%Y-%m-%d %H:%M:%S")
        )
        worked_hours = round((out_dt - in_dt).total_seconds() / 3600, 2)

    return {
        "date": date,
        "employee": employee,
        "in_time": in_time,
        "out_time": out_time,
        "worked_hours": worked_hours,
        "total_punches": len(logs),
    }
