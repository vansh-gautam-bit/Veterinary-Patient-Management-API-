from sqlalchemy import Column, Integer, String , DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Owner(Base):
    __tablename__="owners"

    id = Column(Integer, primary_key=True, index=True)

    name  = Column(String, nullable=False)
    phone  = Column(String, nullable=False)
    email = Column(String, nullable=False)

    created_at = Column(DateTime, unique=True, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime,unique =True, nullable =False, default= datetime.utcnow )

    pets = relationship( "Pet", back_populates="owner")