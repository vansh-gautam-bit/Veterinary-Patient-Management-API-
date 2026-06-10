from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Visit(Base):
    __tablename__="visits"

    id = Column(Integer, primary_key=True, index=True)

    pet_id  = Column(Integer, ForeignKey("pets.id"), nullable=False)
    reason  = Column(String, nullable=False)
    notes = Column(Integer, nullable=True)

    visit_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    pet = relationship("Pet",back_populates="visits")

    pet_id = Column(Integer, ForeignKey("pets.id"),nullable= False)