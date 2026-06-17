from sqlalchemy import Column, String, DateTime
from database import Base
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Enum as SQLEnum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    VET = "VET"
    RECEPTIONIST = "RECEPTIONIST"


class User(Base):
    __tablename__="users"

    id = Column(String,primary_key=True,default=lambda:str(uuid.uuid4()))
    name = Column(String,unique=True,index=True,nullable=False)

    email = Column(String,nullable=False,unique=True,index=True)

    password_hash = Column(String,nullable =False)
    role = Column(SQLEnum(UserRole),nullable=False)
    

    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)

