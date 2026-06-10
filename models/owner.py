from sqlalchemy import Column, Integer, String , DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Owner(Base):
    __tablename__="owners"

    owner_id = Column(Integer, primary_key=True, index=True)

    owner_name  = Column(String, nullable=False)
    phone  = Column(String, nullable=False)
    email = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    pet = relationship( "pet", back_populates="owner")