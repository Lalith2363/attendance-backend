from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.api.deps import get_current_user
from app.services.payroll_service import calculate_payroll, monthly_payroll

router = APIRouter(prefix="/payroll")


@router.get("/{employee_id}")
def get_payroll(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.get("employee_id") != employee_id and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return calculate_payroll(db, employee_id)


@router.get("/{employee_id}/monthly")
def get_monthly_payroll(
    employee_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.get("employee_id") != employee_id and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    return monthly_payroll(db, employee_id, year, month)