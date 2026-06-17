from pydantic import BaseModel,EmailStr
from datetime import datetime
from models.user import UserRole

class UserBase(BaseModel):
    name:str
    email:EmailStr
    password:str
    role: UserRole

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class UserResponse(BaseModel):
    id:str
    name:str
    email:EmailStr
    role:UserRole
    created_at:datetime
    updated_at:datetime

    class Config:
        from_attribute =True
