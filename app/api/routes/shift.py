from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.shift import Shift
from app.schemas.shift import ShiftCreate

router = APIRouter(prefix="/shifts")

@router.post("/")
def create_shift(data: ShiftCreate, db: Session = Depends(get_db)):
    shift = Shift(**data.dict())
    db.add(shift)
    db.commit()
    return shift


@router.get("/")
def get_shifts(db: Session = Depends(get_db)):
    return db.query(Shift).all()