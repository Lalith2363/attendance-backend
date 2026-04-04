from sqlalchemy import Column, Integer, Time, String
from app.db.database import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    start_time = Column(Time)
    end_time = Column(Time)