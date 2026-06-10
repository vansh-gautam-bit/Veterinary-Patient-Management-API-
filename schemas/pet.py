from pydantic import BaseModel
from datetime import datetime

class petupdate(BaseModel):
    name: str
    species: str
    breed: str
    age:int
    owner_name: str
    owner_phone: str



class PetBase(BaseModel):
    name:str
    species:str
    breed:str
    age:int
    owner_name:str
    owner_phone:str

class PetCreate(PetBase):
    pass


class PetResponse(PetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True