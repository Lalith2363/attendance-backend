from sqlalchemy.orm import Session
from datetime import datetime

from app.models.attendance import Attendance
from app.models.employee import Employee


def calculate_payroll(db: Session, employee_id: int):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        return None

    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.check_out != None
    ).all()

    total_hours = 0
    total_overtime = 0

    for r in records:
        duration = r.check_out - r.check_in
        hours = duration.total_seconds() / 3600
        total_hours += hours

        # simple overtime: > 8 hrs/day
        if hours > 8:
            total_overtime += (hours - 8)

    base_pay = total_hours * employee.salary_per_hour
    overtime_pay = total_overtime * employee.overtime_rate

    total_salary = base_pay + overtime_pay

    return {
        "employee_id": employee_id,
        "total_hours": total_hours,
        "overtime_hours": total_overtime,
        "base_pay": base_pay,
        "overtime_pay": overtime_pay,
        "total_salary": total_salary
    }

def monthly_payroll(db: Session, employee_id: int, year: int, month: int):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()

    filtered = []

    for r in records:
        if r.check_in.year == year and r.check_in.month == month:
            filtered.append(r)

    total_hours = 0
    total_overtime = 0

    for r in filtered:
        if r.check_out:
            duration = r.check_out - r.check_in
            hours = duration.total_seconds() / 3600

            total_hours += hours

            if hours > 8:
                total_overtime += (hours - 8)

    base_pay = total_hours * employee.salary_per_hour
    overtime_pay = total_overtime * employee.overtime_rate

    return {
        "month": f"{year}-{month}",
        "total_hours": total_hours,
        "overtime_hours": total_overtime,
        "salary": base_pay + overtime_pay
    }