from pydantic import BaseModel
from datetime import time

class ShiftCreate(BaseModel):
    name: str
    start_time: time
    end_time: time