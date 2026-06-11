from pydantic import BaseModel
from datetime import datetime

class PetUpdate(BaseModel):
    name: str
    species: str
    breed: str
    age:int
    owner_id:int
    
class PetBase(BaseModel):
    name:str
    species:str
    breed:str
    age:int
    owner_id:int

class PetCreate(PetBase):
    pass


class PetResponse(PetBase):
    id: int
    created_at: datetime
    

    class Config:
        from_attributes = True