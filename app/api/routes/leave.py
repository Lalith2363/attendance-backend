from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.leave import Leave
from app.schemas.leave import LeaveCreate

router = APIRouter(prefix="/leaves")

@router.post("/")
def apply_leave(data: LeaveCreate, db: Session = Depends(get_db)):
    leave = Leave(**data.dict())
    db.add(leave)
    db.commit()
    return leave


@router.get("/")
def get_leaves(db: Session = Depends(get_db)):
    return db.query(Leave).all()