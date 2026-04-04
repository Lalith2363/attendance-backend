from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    employee_id: int

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    check_in: datetime
    check_out: datetime | None

    class Config:
        from_attributes = True