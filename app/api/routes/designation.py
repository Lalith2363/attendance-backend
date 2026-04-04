from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.designation import Designation
from app.schemas.designation import DesignationCreate

router = APIRouter(prefix="/designations")

@router.post("/")
def create_designation(data: DesignationCreate, db: Session = Depends(get_db)):
    d = Designation(name=data.name)
    db.add(d)
    db.commit()
    return d


@router.get("/")
def get_designations(db: Session = Depends(get_db)):
    return db.query(Designation).all()