from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.services.report_service import get_employee_report,daily_summary
from app.services.report_service import dashboard_stats

router = APIRouter(prefix="/reports")


@router.get("/employee/{employee_id}")
def employee_report(employee_id: int, db: Session = Depends(get_db)):
    return get_employee_report(db, employee_id)

@router.get("/daily")
def get_daily_summary(db: Session = Depends(get_db)):
    return daily_summary(db)

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    return dashboard_stats(db)