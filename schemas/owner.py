from pydantic import BaseModel
from datetime import datetime

class OwnerUpdate(BaseModel):
    owner_name: str
    phone: str
    email:str



class OwnerBase(BaseModel):
    owner_name: str
    phone: str
    email:str
    
class OwnerCreate(OwnerBase):
    pass


class OwnerResponse(OwnerBase):
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True