from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from datetime import date
from app.models.employee import Employee

def calculate_total_hours(records):
    total_seconds = 0

    for r in records:
        if r.check_out:
            duration = r.check_out - r.check_in
            total_seconds += duration.total_seconds()

    return total_seconds / 3600


def get_employee_report(db: Session, employee_id: int):
    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()

    total_hours = calculate_total_hours(records)

    return {
        "employee_id": employee_id,
        "total_records": len(records),
        "total_hours": total_hours
    }

def daily_summary(db: Session):
    today = date.today()

    records = db.query(Attendance).all()

    today_records = [
        r for r in records if r.check_in.date() == today
    ]

    present = len(today_records)
    completed = len([r for r in today_records if r.check_out])

    return {
        "date": str(today),
        "present": present,
        "completed_sessions": completed
    }

def dashboard_stats(db: Session):

    total_employees = db.query(Employee).count()
    total_attendance = db.query(Attendance).count()

    return {
        "total_employees": total_employees,
        "total_attendance_records": total_attendance
    }