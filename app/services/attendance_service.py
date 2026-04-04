from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.shift import Shift
from app.services.shift_service import evaluate_attendance


# ✅ Check-in
def check_in_employee(db: Session, employee_id: int):

    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.check_out == None
    ).first()

    if existing:
        return None

    record = Attendance(employee_id=employee_id)
    db.add(record)
    db.commit()
    db.refresh(record)

    return record


# ✅ Check-out with shift logic
def check_out_with_shift(db: Session, attendance_id: int, user):

    record = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not record:
        return None

    # 🔒 Ownership check
    if user.get("employee_id") != record.employee_id and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized")

    if record.check_out:
        return None

    record.check_out = datetime.utcnow()

    employee = db.query(Employee).filter(Employee.id == record.employee_id).first()
    shift = db.query(Shift).filter(Shift.id == employee.shift_id).first()

    result = evaluate_attendance(record.check_in, record.check_out, shift)

    db.commit()

    return {
        "attendance_id": record.id,
        "status": result["status"],
        "work_hours": result["work_hours"],
        "overtime": result["overtime"]
    }


# ✅ Get attendance
def get_employee_attendance(db: Session, employee_id: int):
    return db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).all()


# ✅ Calculate total work hours
def calculate_work_hours(db: Session, employee_id: int):

    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.check_out != None
    ).all()

    total_seconds = 0

    for r in records:
        duration = r.check_out - r.check_in
        total_seconds += duration.total_seconds()

    return {
        "employee_id": employee_id,
        "total_hours": total_seconds / 3600
    }