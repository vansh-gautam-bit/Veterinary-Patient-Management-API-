from sqlalchemy import Column, Integer, String , DateTime
from database import Base
from datetime import datetime

class Pet(Base):
    __tablename__="pets"

    id = Column(Integer, primary_key=True, index=True)

    name  = Column(String, nullable=False)
    species  = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    owner_name = Column(String, nullable=False)
    owner_phone = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)