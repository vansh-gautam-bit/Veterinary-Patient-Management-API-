from pydantic import BaseModel
from datetime import datetime

class OwnerBase(BaseModel):
    name: str
    phone: str
    email:str
    

class OwnerUpdate(OwnerBase):
    pass

class OwnerCreate(OwnerBase):
    pass


class OwnerResponse(OwnerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True