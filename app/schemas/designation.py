from pydantic import BaseModel

class DesignationCreate(BaseModel):
    name: str
    