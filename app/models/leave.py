from sqlalchemy import Column, Integer, Date, String, ForeignKey
from app.db.database import Base

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))

    start_date = Column(Date)
    end_date = Column(Date)

    reason = Column(String)
    status = Column(String, default="pending")