from pydantic import BaseModel
from datetime import datetime

class visitBase(BaseModel):
    reason: str
    notes:str

class PetCreate(visitBase):
    pass 

class VisitResponse(visitBase):
    id:int
    pet_id: int
    visit_date: datetime
    created_at: datetime

class Config:
    from_attributes = True    


