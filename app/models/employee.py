from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    department_id = Column(Integer, ForeignKey("departments.id"))
    designation_id = Column(Integer, ForeignKey("designations.id"))
    shift_id= Column(Integer, ForeignKey("shifts.id"))
    salary_per_hour = Column(Integer, default=10)
    overtime_rate = Column(Integer, default=15)