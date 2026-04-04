from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.api.deps import get_current_user, require_admin

router = APIRouter()


# CREATE employee (ADMIN ONLY)
@router.post("/employees", response_model=EmployeeResponse)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    # Prevent duplicate email
    existing = db.query(Employee).filter(Employee.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    employee = Employee(name=data.name, email=data.email)
    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# GET employee by ID
@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# GET all employees (with pagination)
@router.get("/employees", response_model=list[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    employees = db.query(Employee).offset(skip).limit(limit).all()
    return employees


# UPDATE employee (ADMIN ONLY)
@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Check if new email already exists for another user
    existing = db.query(Employee).filter(
        Employee.email == data.email,
        Employee.id != employee_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")

    employee.name = data.name
    employee.email = data.email

    db.commit()
    db.refresh(employee)

    return employee


# DELETE employee (ADMIN ONLY)
@router.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted"}