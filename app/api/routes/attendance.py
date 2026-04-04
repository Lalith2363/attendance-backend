from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.api.deps import get_current_user

from app.services.attendance_service import (
    check_in_employee,
    check_out_with_shift,
    get_employee_attendance,
    calculate_work_hours
)

router = APIRouter()


# ✅ Check-in (SECURE)
@router.post("/attendance/check-in")
def check_in(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    employee_id = user.get("employee_id")

    if not employee_id:
        raise HTTPException(status_code=400, detail="Invalid user")

    result = check_in_employee(db, employee_id)

    if not result:
        raise HTTPException(status_code=400, detail="Already checked in today")

    return result


# ✅ Check-out (WITH SHIFT LOGIC)
@router.post("/attendance/check-out/{attendance_id}")
def check_out(
    attendance_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = check_out_with_shift(db, attendance_id, user)

    if not result:
        raise HTTPException(status_code=400, detail="Invalid or already checked out")

    return result


# ✅ Get attendance (IDOR protected)
@router.get("/attendance/{employee_id}")
def get_attendance(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.get("employee_id") != employee_id and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return get_employee_attendance(db, employee_id)


# ✅ Work hours (secured)
@router.get("/attendance/{employee_id}/hours")
def get_work_hours(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.get("employee_id") != employee_id and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return calculate_work_hours(db, employee_id)