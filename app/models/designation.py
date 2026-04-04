from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True)
    name = Column(String)