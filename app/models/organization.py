from sqlalchemy import Column, Integer, String , TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base    
class Organization(Base):
    __tablename__ = "organizations"
    org_id = Column (Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    relationship = relationship("User", back_populates="organization")
