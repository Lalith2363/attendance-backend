from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.department import Department
from app.schemas.department import DepartmentCreate

router = APIRouter(prefix="/departments")

@router.post("/")
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    dept = Department(name=data.name)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


@router.get("/")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()